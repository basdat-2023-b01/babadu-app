from django.urls import path, include
from base.views import *

urlpatterns = [
    path('', include('base.urls')),
]
