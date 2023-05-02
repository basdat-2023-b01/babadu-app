from django.shortcuts import render

def pertandingan_view(request):
    return render(request, 'pertandingan.html')