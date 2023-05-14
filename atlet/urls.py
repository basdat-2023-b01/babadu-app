from django.urls import path
from atlet.views import *

app_name = 'atlet'

urlpatterns = [
    path('daftar/', daftar_atlet_view, name='daftar'),
    path('lihat/', lihat_atlet_view, name='lihat'),
    path('umpire-daftar-atlet', umpire_daftar_atlet_view, name='umpire-daftar-atlet')
]
