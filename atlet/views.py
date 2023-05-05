from django.shortcuts import render
from atlet.forms import *

def daftar_atlet_view(request):
    context = {
        'daftar_atlet_form': DaftarAtletForm(),
    }
    return render(request, 'daftar_atlet.html', context)

def lihat_atlet_view(request):
    return render(request, 'lihat_atlet.html')