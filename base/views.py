from django.shortcuts import render, redirect
from django.db import connection
from base.helper.function import parse

def main(request):
    if request.session['is_atlet'] or request.session['is_pelatih'] or request.session['is_umpire'] :
        return redirect('dashboard:main')
    return render(request, 'index.html')

