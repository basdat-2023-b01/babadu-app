from atlet.forms import *
from django.shortcuts import render, redirect
from atlet.query import *
from django.db import connection
from base.helper.function import parse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def daftar_atlet_view(request):
    if "id" not in request.session or not request.session['is_pelatih']:
        return redirect('main:main')
    
    query = get_atlet_pelatih_query(request.session['id'])
    cursor = connection.cursor()
    cursor.execute("set search_path to babadu;")
    cursor.execute(query)
    res = parse(cursor)
    atlet = [(atlet['id'], atlet['nama']) for atlet in res]

    form = DaftarAtletForm(atlet, request.POST or None)
    
    if request.method == 'POST' and 'daftar_atlet_submit' in request.POST and form.is_valid():
        id_atlet = form.cleaned_data['daftar_atlet']
        query = insert_atlet_pelatih_query(id_atlet, request.session['id'])
        print(query)
        cursor.execute("set search_path to babadu;")
        cursor.execute(query)
        return redirect('atlet:lihat')
    
    context = {
        'daftar_atlet_form': form,
    }
    return render(request, 'daftar_atlet.html', context)

def pelatih_lihat_atlet_view(request):
    if "id" not in request.session or not request.session['is_pelatih']:
        return redirect('main:main')
    query = get_atlet_dilatih_query(request.session['id'])
    cursor = connection.cursor()
    cursor.execute("set search_path to babadu;")
    cursor.execute(query)
    res = parse(cursor)
    context = {'list_atlet': res}
    return render(request, 'pelatih_lihat_atlet_view.html', context)

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

    context = {
        'atlet_kualifikasi': atlet_kualifikasi,
        'atlet_nonkualifikasi': atlet_nonkualifikasi,
        'atlet_ganda': atlet_ganda
    }

    return render(request, 'umpire_daftar_atlet.html', context)