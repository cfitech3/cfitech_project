"""CFI-TECH — URLs formations"""
from django.urls import path
from . import views

app_name = 'formations'

urlpatterns = [
    path('', views.formation_list, name='list'),
    path('inscription/', views.inscription, name='inscription'),
    path('inscription/succes/<str:reference>/', views.inscription_success, name='inscription_success'),
    path('<slug:slug>/', views.formation_detail, name='detail'),
]
