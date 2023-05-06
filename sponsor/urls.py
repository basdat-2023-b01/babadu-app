from django.urls import path
from sponsor.views import *

app_name = 'sponsor'

urlpatterns = [
    path('daftar/', daftar_sponsor_view, name='daftar'),
]