from django.urls import path, include

urlpatterns = [
    path('', include('base.urls')),
    path('authentication/', include('authentication.urls')),
    path('event/', include('event.urls')),
    path('hasil-pertandingan/', include('hasil_pertandingan.urls')),
    path('dashboard/', include('dashboard.urls')),
]
