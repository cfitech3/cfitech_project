"""CFI-TECH — URLs core"""
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('a-propos/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('galerie/', views.gallery, name='gallery'),
    path('temoignages/', views.testimonials_view, name='testimonials'),
    path('partenaires/', views.partners_view, name='partners'),
    path('noor-energy/', views.noor_energy, name='noor_energy'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('newsletter/inscription/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('robots.txt', views.robots_txt),
]
