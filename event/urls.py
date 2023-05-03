from django.urls import path
from event.views import *

app_name = 'event'

urlpatterns = [
    path('', event_view, name='main'),
]
