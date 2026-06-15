"""CFI-TECH — Vues des formations"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
import requests

from .models import Domain, Formation, Inscription
from core.models import SiteConfig


def formation_list(request):
    """Liste des formations avec filtrage"""
    config = SiteConfig.get_config()
    formations = Formation.objects.filter(is_active=True).select_related('domain', 'trainer')

    # Filtres
    domain_slug = request.GET.get('domaine', '')
    level = request.GET.get('niveau', '')
    status = request.GET.get('statut', '')
    search = request.GET.get('q', '')

    if domain_slug:
        formations = formations.filter(domain__slug=domain_slug)
    if level:
        formations = formations.filter(level=level)
    if status:
        formations = formations.filter(status=status)
    if search:
        formations = formations.filter(title__icontains=search)

    paginator = Paginator(formations, 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    domains = Domain.objects.filter(is_active=True).order_by('display_order')

    return render(request, 'formations/list.html', {
        'config': config,
        'page_obj': page_obj,
        'domains': domains,
        'current_domain': domain_slug,
        'current_level': level,
        'current_status': status,
        'search_query': search,
        'page_title': 'Nos Formations — CFI-TECH',
    })


def formation_detail(request, slug):
    """Détail d'une formation"""
    config = SiteConfig.get_config()
    formation = get_object_or_404(Formation, slug=slug, is_active=True)
    formation.views_count += 1
    formation.save(update_fields=['views_count'])
    related = Formation.objects.filter(domain=formation.domain, is_active=True).exclude(pk=formation.pk)[:4]

    return render(request, 'formations/detail.html', {
        'config': config,
        'formation': formation,
        'related': related,
        'page_title': f'{formation.title} — CFI-TECH',
    })


def inscription(request):
    """Formulaire d'inscription général"""
    config = SiteConfig.get_config()
    formations_open = Formation.objects.filter(is_active=True).order_by('title')
    formation_slug = request.GET.get('formation', '')
    preselected = None
    if formation_slug:
        preselected = Formation.objects.filter(slug=formation_slug, is_active=True).first()

    if request.method == 'POST':
        return _handle_inscription(request, config, formations_open, preselected)

    return render(request, 'formations/inscription.html', {
        'config': config,
        'formations': formations_open,
        'preselected': preselected,
        'level_choices': Inscription.LEVELS,
        'page_title': 'Inscription — CFI-TECH',
    })


def _handle_inscription(request, config, formations_open, preselected):
    """Traitement du formulaire d'inscription"""
    last_name = request.POST.get('last_name', '').strip()
    first_name = request.POST.get('first_name', '').strip()
    phone = request.POST.get('phone', '').strip()
    email = request.POST.get('email', '').strip()
    formation_id = request.POST.get('formation', '')
    level = request.POST.get('level', 'lycee')
    message = request.POST.get('message', '').strip()

    errors = []
    if not last_name:
        errors.append('Le nom est obligatoire.')
    if not first_name:
        errors.append('Le prénom est obligatoire.')
    if not phone:
        errors.append('Le numéro de téléphone est obligatoire.')
    if not formation_id:
        errors.append('Veuillez sélectionner une formation.')

    formation = None
    if formation_id:
        try:
            formation = Formation.objects.get(pk=formation_id, is_active=True)
            if not formation.is_registration_open:
                errors.append(f'Les inscriptions pour "{formation.title}" sont fermées.')
        except Formation.DoesNotExist:
            errors.append('Formation introuvable.')

    if errors:
        for error in errors:
            messages.error(request, error)
        return render(request, 'formations/inscription.html', {
            'config': config,
            'formations': formations_open,
            'preselected': preselected,
            'level_choices': Inscription.LEVELS,
            'page_title': 'Inscription — CFI-TECH',
        })

    # Créer l'inscription
    ins = Inscription.objects.create(
        last_name=last_name,
        first_name=first_name,
        phone=phone,
        email=email or '',
        formation=formation,
        level=level,
        message=message,
    )

    # Mettre à jour le compteur
    if formation:
        Formation.objects.filter(pk=formation.pk).update(
            registered_count=formation.registered_count + 1
        )

    # Envoyer email de confirmation
    if email:
        try:
            send_mail(
                subject='✅ Inscription confirmée — CFI-TECH',
                message=f"""Bonjour {first_name} {last_name},

Votre inscription à la formation "{formation.title}" a bien été reçue.

📋 Référence : {ins.reference}
📞 Formation : {formation.title}
📅 Début : {formation.start_date or 'À confirmer'}
💰 Prix : {formation.get_price_display()}

Notre équipe vous contactera dans les plus brefs délais pour confirmer votre place.

Pour toute question : {settings.CFITECH_PHONE}
WhatsApp : {settings.CFITECH_WHATSAPP}

Cordialement,
L'équipe CFI-TECH
Apprenez, Innovez, Réussissez !
""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=True,
            )
        except Exception:
            pass

    # Envoyer notification admin
    try:
        send_mail(
            subject=f'🔔 Nouvelle inscription : {first_name} {last_name} — {formation.title}',
            message=f"""Nouvelle inscription reçue !

Référence : {ins.reference}
Candidat : {first_name} {last_name}
Téléphone : {phone}
Email : {email or 'Non fourni'}
Formation : {formation.title}
Niveau : {ins.get_level_display()}
Message : {message or 'Aucun'}
Date : {ins.created_at.strftime('%d/%m/%Y %H:%M')}
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CFITECH_EMAIL],
            fail_silently=True,
        )
    except Exception:
        pass

    # Synchronisation Google Sheets
    if getattr(settings, 'GOOGLE_SCRIPT_URL', ''):
        try:
            from django.utils import timezone
            now_str = timezone.now().strftime('%d/%m/%Y %H:%M')
            print(f"📤 Envoi vers Google Sheets...")
            response = requests.post(
                settings.GOOGLE_SCRIPT_URL,
                json={
                    'reference': ins.reference,
                    'nom':       last_name,
                    'prenom':    first_name,
                    'telephone': phone,
                    'email':     email,
                    'formation': formation.title if formation else '',
                    'niveau':    ins.get_level_display(),
                    'message':   message,
                    'date':      now_str,
                },
                timeout=10
            )
            print(f"📥 Réponse : {response.status_code} — {response.text}")
            Inscription.objects.filter(pk=ins.pk).update(synced_to_sheets=True)
        except Exception as e:
            print(f"❌ Erreur Google Sheets : {e}")# Synchronisation Google Sheets
    if getattr(settings, 'GOOGLE_SCRIPT_URL', ''):
        try:
            from django.utils import timezone
            now_str = timezone.now().strftime('%d/%m/%Y %H:%M')
            print(f"📤 Envoi vers Google Sheets...")
            response = requests.post(
                settings.GOOGLE_SCRIPT_URL,
                json={
                    'reference': ins.reference,
                    'nom':       last_name,
                    'prenom':    first_name,
                    'telephone': phone,
                    'email':     email,
                    'formation': formation.title if formation else '',
                    'niveau':    ins.get_level_display(),
                    'message':   message,
                    'date':      now_str,
                },
                timeout=10
            )
            print(f"📥 Réponse : {response.status_code} — {response.text}")
            Inscription.objects.filter(pk=ins.pk).update(synced_to_sheets=True)
        except Exception as e:
            print(f"❌ Erreur Google Sheets : {e}")


    messages.success(
            request,
            f"Votre inscription à {formation.title} a été enregistrée avec succès."
        )

    return redirect(
            'formations:inscription_success',
            reference=ins.reference
        )

# Dans _handle_inscription(), remplacez le bloc Google Sheets par :
    # if getattr(settings, 'GOOGLE_SCRIPT_URL', ''):
    #     try:
    #         print(f"📤 Envoi vers Google Sheets : {settings.GOOGLE_SCRIPT_URL}")
    #         response = requests.post(settings.GOOGLE_SCRIPT_URL, json={
    #             'reference': ins.reference,
    #             'nom':       last_name,
    #             'prenom':    first_name,
    #             'telephone': phone,
    #             'email':     email,
    #             'formation': formation.title if formation else '',
    #             'niveau':    ins.get_level_display(),
    #             'message':   msg,
    #             'date':      ins.created_at.strftime('%d/%m/%Y %H:%M'),
    #         }, timeout=10)
    #         print(f"📥 Réponse Google : {response.status_code} — {response.text}")
    #         Inscription.objects.filter(pk=ins.pk).update(synced_to_sheets=True)
    #     except Exception as e:
    #         print(f"❌ Erreur Google Sheets : {e}")
    # else:
    #     print("⚠️  GOOGLE_SCRIPT_URL non configuré dans .env")
def inscription_success(request, reference):
    """Page de confirmation d'inscription"""
    config = SiteConfig.get_config()
    ins = get_object_or_404(Inscription, reference=reference)
    return render(request, 'formations/inscription_success.html', {
        'config': config,
        'inscription': ins,
        'page_title': 'Inscription confirmée — CFI-TECH',
    })
