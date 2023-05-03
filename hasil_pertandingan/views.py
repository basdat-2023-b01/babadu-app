from django.shortcuts import render

def hasil_pertandingan_view(request):
    return render(request, 'hasil_pertandingan.html')