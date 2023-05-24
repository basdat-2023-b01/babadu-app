from django.urls import path
from event.views import *

app_name = 'event'

urlpatterns = [
    path('lihat/', lihat_event_view, name='lihat'),
    path('lihat/pertandingan/<uuid:id>/', pertandingan_view, name='pertandingan'),
    path('daftar/', daftar_stadium_view, name='daftar'),
    path('daftar/<slug:stadium>/', daftar_event_view, name='daftar-event'),
    path('daftar/<slug:stadium>/<slug:event>/<int:tahun>', daftar_partai_kompetisi, name='daftar-partai-kompetisi'),
    path('lihat/enrolled-partai-kompetisi-event', enrolled_partai_kompetisi_event_view, name='lihat-enrolled-partai-kompetisi-event'),
    path('lihat/enrolled-event', enrolled_event_view, name='lihat-enrolled-event')
]
