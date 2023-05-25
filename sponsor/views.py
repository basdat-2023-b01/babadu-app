from django.shortcuts import render, redirect
from sponsor.forms import *
from datetime import datetime
from sponsor.query import *
from django.db import connection, InternalError
from base.helper.function import parse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def daftar_sponsor_view(request):
    if "id" not in request.session or not request.session['is_atlet']:
        return redirect('main:main')
    
    query = daftar_sponsor_query(request.session['id'])
    cursor = connection.cursor()
    cursor.execute("set search_path to babadu;")
    cursor.execute(query)
    res = parse(cursor)
    sponsor = [(sponsor['id'], sponsor['nama_brand']) for sponsor in res]

    form = DaftarSponsorForm(sponsor, request.POST or None)
    
    if request.method == 'POST' and 'daftar_sponsor_submit' in request.POST and form.is_valid():
        id_sponsor = form.cleaned_data['daftar_sponsor']
        tgl_mulai = request.POST.get('tgl_mulai')
        tgl_selesai = request.POST.get('tgl_selesai')
        query = insert_atlet_sponsor_query(request.session['id'], id_sponsor, tgl_mulai, tgl_selesai)
        cursor.execute("set search_path to babadu;")
        cursor.execute(query)
        return redirect('sponsor:list-sponsor')
    
    context = {
        'daftar_sponsor_form': form,
    }
    return render(request, 'daftar_sponsor.html', context)

def list_sponsor_view(request):
    if "id" not in request.session or not request.session['is_atlet']:
        return redirect('main:main')
    
    query = get_list_sponsor_query(request.session['id'])
    cursor = connection.cursor()
    cursor.execute("set search_path to babadu;")
    cursor.execute(query)
    res = parse(cursor)
    context = {'list_sponsor': res}
    return render(request, 'list_sponsor.html', context)