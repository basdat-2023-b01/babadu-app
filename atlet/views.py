from atlet.forms import *
from django.shortcuts import render, redirect
from atlet.query import *
from django.db import connection
from base.helper.function import parse

def daftar_atlet_view(request):
    context = {
        'daftar_atlet_form': DaftarAtletForm(),
    }
    return render(request, 'daftar_atlet.html', context)

def lihat_atlet_view(request):
    return render(request, 'lihat_atlet.html')

def umpire_daftar_atlet_view(request):
    if "id" not in request.session or not request.session['is_umpire']:
        return redirect('main:main')
    
    query_kualifikasi = get_all_atlet_kualifikasi_query()
    query_nonkualifikasi = get_all_atlet_nonkualifikasi_query()
    query_ganda =  get_all_atlet_ganda_query()

    cursor = connection.cursor()
    cursor.execute("set search_path to babadu;")

    cursor.execute(query_kualifikasi)
    atlet_kualifikasi = parse(cursor)

    cursor.execute(query_nonkualifikasi)
    atlet_nonkualifikasi = parse(cursor)

    cursor.execute(query_ganda)
    atlet_ganda = parse(cursor)

    print(atlet_ganda)

    context = {
        'atlet_kualifikasi': atlet_kualifikasi,
        'atlet_nonkualifikasi': atlet_nonkualifikasi,
        'atlet_ganda': atlet_ganda
    }

    return render(request, 'umpire_daftar_atlet.html', context)