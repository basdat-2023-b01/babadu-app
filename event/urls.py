from django.urls import path
from event.views import *

app_name = 'event'

urlpatterns = [
    path('lihat/', lihat_event_view, name='lihat'),
    path('lihat/pertandingan/<uuid:id>/', pertandingan_view, name='pertandingan'),
    path('daftar/', daftar_stadium_view, name='daftar'),
    path('daftar/<uuid:id>/', daftar_event_view, name='daftar-event'),
    path('daftar/<uuid:id1>/kategori/<uuid:id2>', daftar_kategori_view, name='daftar-kategori'),
    path('lihat/enrolled-event', enrolled_event_view, name='lihat-enrolled-event')
]
