"""CFI-TECH — Sitemaps pour SEO"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from formations.models import Formation
from .models import BlogPost


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return ['core:home', 'core:about', 'core:contact', 'core:faq',
                'formations:list', 'formations:inscription', 'services:list',
                'core:partners', 'core:noor_energy', 'core:blog_list']

    def location(self, item):
        return reverse(item)


class FormationSitemap(Sitemap):
    priority = 0.9
    changefreq = 'daily'

    def items(self):
        return Formation.objects.filter(is_active=True)

    def location(self, obj):
        return obj.get_absolute_url()

    def lastmod(self, obj):
        return obj.updated_at


class BlogSitemap(Sitemap):
    priority = 0.7
    changefreq = 'weekly'

    def items(self):
        return BlogPost.objects.filter(status='published')

    def location(self, obj):
        return obj.get_absolute_url()

    def lastmod(self, obj):
        return obj.updated_at
