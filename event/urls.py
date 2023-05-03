from django.urls import path
from event.views import *

app_name = 'event'

urlpatterns = [
    path('', main, name='main'),
    path('<uuid:id>/', daftar_event, name='get-daftar-event'),
    path('<uuid:id1>/daftar-kategori/<uuid:id2>', daftar_kategori, name='get-daftar-kategori'),
    path('pertandingan/<uuid:id>', pertandingan, name='pertandingan')
]
