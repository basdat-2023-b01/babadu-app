from django.shortcuts import render
from tes_kualifikasi.forms import *

def data_kualifikasi_view(request):
    context = {
        'data_kualifikasi_form': DataKualifikasiForm(),
    }
    return render(request, 'data_kualifikasi.html', context)

def pertanyaan_kualifikasi_view(request):
    context = {
        'pertanyaan_kualifikasi_form': PertanyaanKualifikasiForm(),
    }
    return render(request, 'pertanyaan_kualifikasi.html', context)