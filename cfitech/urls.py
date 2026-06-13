"""CFI-TECH — Configuration des URLs principales"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from core.sitemaps import StaticViewSitemap, FormationSitemap, BlogSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'formations': FormationSitemap,
    'blog': BlogSitemap,
}

# Personnalisation de l'admin Django
admin.site.site_header = 'CFI-TECH Administration'
admin.site.site_title = 'CFI-TECH Admin'
admin.site.index_title = 'Tableau de bord CFI-TECH'

urlpatterns = [
    path('cfitech-admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    # Applications
    path('', include('core.urls')),
    path('formations/', include('formations.urls')),
    path('services/', include('services.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
