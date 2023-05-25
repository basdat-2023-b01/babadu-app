from django.urls import path, include

urlpatterns = [
    path('', include('base.urls')),
    path('authentication/', include('authentication.urls')),
    path('event/', include('event.urls')),
    path('hasil-pertandingan/', include('hasil_pertandingan.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('tes-kualifikasi/', include('tes_kualifikasi.urls')),
    path('atlet/', include('atlet.urls')),
    path('sponsor/', include('sponsor.urls')),
    path('pertandingan/', include('pertandingan.urls')),
]
