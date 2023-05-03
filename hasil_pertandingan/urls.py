from django.urls import path
from hasil_pertandingan.views import *

app_name = 'hasil-pertandingan'

urlpatterns = [
    path('', hasil_pertandingan_view, name='main'),
]
