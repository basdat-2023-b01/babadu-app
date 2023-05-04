from django.shortcuts import render

def daftar_atlet_view(request):
    return render(request, 'daftar_atlet.html')

def lihat_atlet_view(request):
    return render(request, 'lihat_atlet.html')