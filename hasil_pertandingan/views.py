from django.shortcuts import render

def hasil_pertandingan_view(request):
    return render(request, 'hasil_pertandingan_main.html')

def hasil_pertandingan_detail_view(request, id):
    return render(request, 'hasil_pertandingan_detail.html')