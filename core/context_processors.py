"""CFI-TECH — Context processors & Sitemaps"""
from .models import SiteConfig
from .models import SiteConfig, Partner


def site_config(request):
    """Injecte la configuration du site dans tous les templates"""
    return {'site_config': SiteConfig.get_config()}


def site_config(request):
    partners = Partner.objects.filter(
        is_active=True, is_noor_energy=False
    ).order_by('display_order')[:8]
    return {
        'site_config': SiteConfig.get_config(),
        'partners':    partners,
    }