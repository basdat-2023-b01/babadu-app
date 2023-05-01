from django.urls import path
from base.views import *

app_name = 'main'

urlpatterns = [
    path('', main, name='main'),
]
