from django.urls import path, include

urlpatterns = [
    path('', include('base.urls')),
    path('authentication/', include('authentication.urls')),
]
