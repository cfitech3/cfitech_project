from django.shortcuts import render
from .models import Service, Logiciel
from core.models import SiteConfig


def service_list(request):
    config   = SiteConfig.get_config()
    services = Service.objects.filter(is_active=True).order_by('display_order')
    return render(request, 'services/list.html', {
        'config':     config,
        'services':   services,
        'page_title': 'Nos Services — CFI-TECH',
    })


def logiciels(request):
    config    = SiteConfig.get_config()
    category  = request.GET.get('categorie', '')

    logiciels_qs = Logiciel.objects.filter(is_active=True)
    if category:
        logiciels_qs = logiciels_qs.filter(category=category)

    # Grouper par catégorie
    from itertools import groupby
    all_logiciels = logiciels_qs.order_by('category', 'display_order')
    grouped = {}
    for logiciel in all_logiciels:
        cat = logiciel.get_category_display()
        if cat not in grouped:
            grouped[cat] = []
        grouped[cat].append(logiciel)

    categories = Logiciel.CATEGORIES

    return render(request, 'services/logiciels.html', {
        'config':          config,
        'grouped':         grouped,
        'all_logiciels':   all_logiciels,
        'categories':      categories,
        'current_category': category,
        'page_title':      'Nos Logiciels — CFI-TECH',
    })