from django.urls import path
from tes_kualifikasi.views import *

app_name = 'tes-kualifikasi'

urlpatterns = [
    path('buat-ujian-kualifikasi/', buat_ujian_kualifikasi_view, name='buat-ujian-kualifikasi'),
    path('umpire-list-ujian-kualifikasi/', umpire_list_ujian_kualifikasi_view, name='umpire-list-ujian-kualifikasi'),
    path('atlet-list-ujian-kualifikasi/', atlet_list_ujian_kualifikasi_view, name='atlet-list-ujian-kualifikasi'),
    path('atlet-list-ujian-kualifikasi/<int:tahun>/<int:batch>/<slug:tempat>/<slug:tanggal>/', pertanyaan_kualifikasi_view, name='pertanyaan-kualifikasi'),
    path('umpire-riwayat-ujian-kualifikasi/', umpire_riwayat_ujian_kualifikasi_view, name='umpire-riwayat-ujian-kualifikasi'),
    path('atlet-riwayat-ujian-kualifikasi/', atlet_riwayat_ujian_kualifikasi_view, name='atlet-riwayat-ujian-kualifikasi')
]
