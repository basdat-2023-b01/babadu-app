from django.shortcuts import render
from sponsor.forms import *
from datetime import datetime

# Create your views here.
def daftar_sponsor_view(request):
    context = {
        'daftar_sponsor_form': DaftarSponsorForm(),
    }
    return render(request, 'daftar_sponsor.html', context)
