from django.urls import path
from tes_kualifikasi.views import *

app_name = 'tes-kualifikasi'

urlpatterns = [
    path('daftar-tes/', data_kualifikasi_view, name='data-kualifikasi'),
    path('pertanyaan/', pertanyaan_kualifikasi_view, name='pertanyaan'),
]
