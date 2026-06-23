"""CFI-TECH — Vues principales (core)"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
from services.models import Logiciel
import requests

from .models import SiteConfig, Partner, Testimonial, FAQ, BlogPost, GalleryItem, TeamMember, NewsletterSubscriber
from formations.models import Formation, Domain


def home(request):
    config = SiteConfig.get_config()

    featured_formations = Formation.objects.filter(
        is_active=True
    ).order_by('-is_featured', '-created_at')[:8]

    open_formations = Formation.objects.filter(
        status='open', is_active=True
    ).order_by('registration_deadline')[:4]

    testimonials = Testimonial.objects.filter(
        is_active=True, is_featured=True
    )[:6]
    partners = Partner.objects.filter(
        is_active=True, is_noor_energy=False
    ).order_by('display_order')[:8]
    recent_posts = BlogPost.objects.filter(
        status='published'
    ).order_by('-published_at')[:3]
    domains = Domain.objects.filter(
        is_active=True
    ).order_by('display_order')

    # ✅ Logiciels mis en avant
    logiciels_home = Logiciel.objects.filter(
        is_active=True, is_featured=True
    ).order_by('display_order')[:8]

    return render(request, 'home.html', {
        'config':            config,
        'featured_formations': featured_formations,
        'open_formations':   open_formations,
        'testimonials':      testimonials,
        'partners':          partners,
        'recent_posts':      recent_posts,
        'domains':           domains,
        'logiciels_home':    logiciels_home,
        'page_title':        "CFI-TECH — Centre de Formation et d'Innovation Technologique",
    })
def about(request):
    """Page À propos"""
    config = SiteConfig.get_config()
    team = TeamMember.objects.filter(is_active=True).order_by('display_order')
    return render(request, 'about.html', {
        'config': config,
        'team': team,
        'page_title': 'À Propos — CFI-TECH',
    })


def contact(request):
    """Page Contact avec formulaire"""
    config = SiteConfig.get_config()

    if request.method == 'POST':
        # Protection honeypot
        if request.POST.get('website_url', '').strip():
            messages.success(request, 'Message envoyé !')
            return redirect('core:contact')

        name    = request.POST.get('name', '').strip()
        email   = request.POST.get('email', '').strip()
        phone   = request.POST.get('phone', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if name and message:
            # ✅ Sauvegarder en base de données
            from .models import ContactMessage
            ContactMessage.objects.create(
                name       = name,
                email      = email,
                phone      = phone,
                subject    = subject,
                message    = message,
                ip_address = request.META.get('REMOTE_ADDR'),
            )

            # Envoyer email notification admin
            try:
                send_mail(
                    subject=f'[CFI-TECH Contact] {subject or "Message depuis le site"}',
                    message=f'Nom : {name}\nEmail : {email}\nTéléphone : {phone}\n\n{message}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CFITECH_EMAIL],
                    fail_silently=True,
                )
            except Exception:
                pass

            messages.success(
                request,
                '✅ Votre message a été envoyé ! Nous vous répondrons dans les meilleurs délais.'
            )
            return redirect('core:contact')
        else:
            messages.error(request, 'Veuillez remplir les champs obligatoires.')

    return render(request, 'contact.html', {
        'config':     config,
        'page_title': 'Contact — CFI-TECH',
    })


def faq(request):
    """FAQ"""
    config = SiteConfig.get_config()
    faqs_by_category = {}
    for faq_item in FAQ.objects.filter(is_active=True).order_by('category', 'display_order'):
        cat = faq_item.get_category_display()
        if cat not in faqs_by_category:
            faqs_by_category[cat] = []
        faqs_by_category[cat].append(faq_item)

    return render(request, 'faq.html', {
        'config': config,
        'faqs_by_category': faqs_by_category,
        'page_title': 'FAQ — CFI-TECH',
    })


def gallery(request):
    """Galerie"""
    config = SiteConfig.get_config()
    items = GalleryItem.objects.filter(is_active=True).order_by('display_order', '-created_at')
    return render(request, 'galerie.html', {
        'config': config,
        'items': items,
        'page_title': 'Galerie — CFI-TECH',
    })


def testimonials_view(request):
    """Témoignages"""
    config = SiteConfig.get_config()
    testimonials = Testimonial.objects.filter(is_active=True).order_by('-is_featured', '-created_at')
    return render(request, 'temoignages.html', {
        'config': config,
        'testimonials': testimonials,
        'page_title': 'Témoignages — CFI-TECH',
    })


def partners_view(request):
    """Partenaires"""
    config = SiteConfig.get_config()
    partners = Partner.objects.filter(is_active=True, is_noor_energy=False).order_by('display_order')
    return render(request, 'partenaires/list.html', {
        'config': config,
        'partners': partners,
        'page_title': 'Nos Partenaires — CFI-TECH',
    })


def noor_energy(request):
    """Page Noor Energy"""
    from .models import NoorEnergyService
    config = SiteConfig.get_config()
    noor_partner = Partner.objects.filter(is_noor_energy=True, is_active=True).first()
    services = NoorEnergyService.objects.filter(is_active=True).order_by('display_order')
    return render(request, 'services/noor_energy.html', {
        'config': config,
        'noor_partner': noor_partner,
        'services': services,
        'page_title': 'Partenariat Noor Energy — CFI-TECH',
    })


def blog_list(request):
    """Liste des articles de blog"""
    config = SiteConfig.get_config()
    post_list = BlogPost.objects.filter(status='published').order_by('-published_at')
    category = request.GET.get('category', '')
    if category:
        post_list = post_list.filter(category=category)

    paginator = Paginator(post_list, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    categories = BlogPost.objects.filter(status='published').values_list('category', flat=True).distinct()

    return render(request, 'blog/list.html', {
        'config': config,
        'page_obj': page_obj,
        'categories': categories,
        'current_category': category,
        'page_title': 'Actualités & Blog — CFI-TECH',
    })


def blog_detail(request, slug):
    """Détail d'un article"""
    config = SiteConfig.get_config()
    post = get_object_or_404(BlogPost, slug=slug, status='published')
    post.views_count += 1
    post.save(update_fields=['views_count'])
    related_posts = BlogPost.objects.filter(status='published').exclude(pk=post.pk)[:3]
    return render(request, 'blog/detail.html', {
        'config': config,
        'post': post,
        'related_posts': related_posts,
        'page_title': f'{post.title} — CFI-TECH',
    })


@require_POST
def newsletter_subscribe(request):
    """Inscription newsletter (AJAX)"""
    email = request.POST.get('email', '').strip()
    name = request.POST.get('name', '').strip()
    if email:
        sub, created = NewsletterSubscriber.objects.get_or_create(email=email, defaults={'full_name': name})
        if created:
            return JsonResponse({'status': 'success', 'message': 'Merci ! Vous êtes inscrit à notre newsletter.'})
        else:
            return JsonResponse({'status': 'info', 'message': 'Vous êtes déjà inscrit à notre newsletter.'})
    return JsonResponse({'status': 'error', 'message': 'Veuillez entrer un email valide.'})


def robots_txt(request):
    """Fichier robots.txt pour SEO"""
    from django.http import HttpResponse
    content = """User-agent: *
Allow: /
Disallow: /cfitech-admin/
Disallow: /ckeditor/

Sitemap: https://cfitech.ml/sitemap.xml
"""
    return HttpResponse(content, content_type='text/plain')




def partner_detail(request, slug):
    """Page détail d'un partenaire"""
    config  = SiteConfig.get_config()
    partner = get_object_or_404(Partner, slug=slug, is_active=True)
    return render(request, 'partenaires/detail.html', {
        'config':     config,
        'partner':    partner,
        'page_title': f'{partner.name} — CFI-TECH',
    })