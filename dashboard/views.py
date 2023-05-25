from django.shortcuts import render, redirect
from django.db import connection
from base.helper.function import parse
from dashboard.query import *

def dashboard_view(request):
    if "id" not in request.session:
        return redirect('authentication:login')
    
    context = {}
    
    if request.session['is_atlet']:
        cursor = connection.cursor()
        cursor.execute("set search_path to babadu;")
        query = get_atlet_detail_query(request.session['id'])
        cursor.execute(query)
        res = parse(cursor)[0]
        for attr in res:
            context[attr] = res[attr]
        
        query = get_atlet_pelatih_detail_query(request.session['id'])
        cursor.execute(query)
        res = parse(cursor)
        pelatih = []
        for p in res:
            pelatih.append(p['nama_pelatih'])
        pelatih = ', '.join(pelatih)
        context['pelatih'] = pelatih
        if context['status_kualifikasi'] == 'Qualified':
            request.session['is_terkualifikasi'] = True
            query = get_atlet_kualifikasi_detail_query(request.session['id'])
            cursor.execute(query)
            context['total_point'] = parse(cursor)[0]['total_points']
        else:
            request.session['is_terkualifikasi'] = False
            
    elif request.session['is_pelatih']:
        cursor = connection.cursor()
        cursor.execute("set search_path to babadu;")
        query = get_pelatih_spesialisasi_detail_query(request.session['id'])
        cursor.execute(query)
        res = parse(cursor)
        spesialisasi = []
        for s in res:
            spesialisasi.append(s['spesialisasi'])
        spesialisasi = ', '.join(spesialisasi)
        context['spesialisasi'] = spesialisasi
    else:
        pass

    return render(request, 'dashboard.html', context)
