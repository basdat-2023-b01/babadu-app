from django.urls import path
from event.views import *
from pertandingan.views import *

app_name = 'pertandingan'

urlpatterns = [
    path('', partai_kompetisi_view, name='lihat-partai-kompetisi'),
    path('<slug:event>/<int:tahun>/<slug:jenis_partai>/<slug:jenis_babak>/', pertandingan_view, name='lihat-partai-kompetisi'),
]
