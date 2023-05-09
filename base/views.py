from django.shortcuts import render, redirect
from django.db import connection
from base.helper.function import parse

def main(request):
    if 'is_atlet' in request.session or 'is_pelatih' in request.session or 'is_umpire' in request.session:
        return redirect('dashboard:main')
    return render(request, 'index.html')

