from django.urls import path
from sponsor.views import *

app_name = 'sponsor'

urlpatterns = [
    path('daftar-sponsor/', daftar_sponsor_view, name='daftar-sponsor'),
    path('list-sponsor/', list_sponsor_view, name='list-sponsor'),
] 