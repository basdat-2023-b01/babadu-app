from django.shortcuts import render


def lihat_event_view(request):
    return render(request, 'lihat_event.html')

def daftar_stadium_view(request):
    return render(request, 'daftar_stadium.html')

def daftar_event_view(request, id):
    return render(request, 'daftar_event.html')


def daftar_kategori_view(request, id1, id2):
    return render(request, 'daftar_kategori.html')

def enrolled_event_view(request):
    return render(request, 'enrolled_event.html')


def pertandingan_view(request, id):
    return render(request, 'pertandingan.html')
