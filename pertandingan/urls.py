from django.urls import path
from pertandingan.views import *

app_name = 'authentication'

urlpatterns = [
    path('', pertandingan_view, name='pertandingan'),
]
