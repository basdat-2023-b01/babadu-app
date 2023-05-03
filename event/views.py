from django.shortcuts import render


def main(request):
    return render(request, 'event_main.html')


def daftar_event(request, id):
    return render(request, 'daftar_event.html')


def daftar_kategori(request, id1, id2):
    return render(request, 'daftar_kategori.html')


def pertandingan(request, id):
    return render(request, 'pertandingan.html')
