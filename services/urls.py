"""CFI-TECH — URLs services"""

from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('',           views.service_list, name='list'),
    path('logiciels/', views.logiciels,    name='logiciels'),
]