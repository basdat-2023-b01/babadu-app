from django.shortcuts import render, redirect
from tes_kualifikasi.forms import *
from tes_kualifikasi.query import *
from django.db import connection, InternalError
from base.helper.function import parse
from tes_kualifikasi.helper import *
from django.contrib import messages
import datetime

def buat_ujian_kualifikasi_view(request):
    if "id" not in request.session or not request.session['is_umpire']:
        return redirect('main:main')
    
    cursor = connection.cursor()
    form = BuatUjianKualifikasi()
    
    if request.method == 'POST' and 'buat_ujian_kualifikasi_submit' in request.POST:
        tahun = request.POST.get('tahun')
        batch = request.POST.get('batch')
        tempat_pelaksanaan = request.POST.get('tempat_pelaksanaan')
        tanggal_pelaksanaan = request.POST.get('tanggal_pelaksanaan')
        query = insert_ujian_kualifikasi_query(tahun, batch, tempat_pelaksanaan, tanggal_pelaksanaan)
        cursor.execute("set search_path to babadu;")
        cursor.execute(query)
        return redirect('tes-kualifikasi:umpire-list-ujian-kualifikasi')
    
    context = {
        'buat_ujian_kualifikasi': form,
    }

    return render(request, 'buat_ujian_kualifikasi.html', context)

def umpire_list_ujian_kualifikasi_view(request):
    if "id" not in request.session or not request.session['is_umpire']:
        return redirect('main:main')
    
    query = get_list_ujian_kualifikasi_query()
    cursor = connection.cursor()
    cursor.execute("set search_path to babadu;")
    cursor.execute(query)
    res = parse(cursor)
    context = {'list_ujian_kualifikasi': res}
    return render(request, 'list_ujian_kualifikasi.html', context)

def atlet_list_ujian_kualifikasi_view(request):
    if "id" not in request.session or not request.session['is_atlet']:
        return redirect('main:main')
    
    query = get_list_ujian_kualifikasi_query()
    cursor = connection.cursor()
    cursor.execute("set search_path to babadu;")
    cursor.execute(query)
    res = parse(cursor)
    list_ujian_kualifikasi = []
    for item in res:
        item['tempat_url'] = convert_to_slug(item['tempat'])
        for attr in item:
            if isinstance(item[attr], datetime.date):
                date = datetime.datetime.strptime(str(item[attr]), '%Y-%m-%d')
                formatted_date = date.strftime('%d %B %Y')
                item[attr] = formatted_date
        item['tanggal_url'] = convert_to_slug(item['tanggal'])
        list_ujian_kualifikasi.append(item)

    context = {'list_ujian_kualifikasi': list_ujian_kualifikasi}

    return render(request, 'list_ujian_kualifikasi.html', context)

def pertanyaan_kualifikasi_view(request, tahun, batch, tempat, tanggal):
    if "id" not in request.session or not request.session['is_atlet']:
        return redirect('main:main')

    tempat = convert_to_title(tempat)
    tanggal = convert_to_date(tanggal)

    cursor = connection.cursor()
    cursor.execute("set search_path to babadu;")
    form = PertanyaanKualifikasiForm()
    
    if request.method == 'POST' and 'pertanyaan_kualifikasi_submit' in request.POST:
        nomor_satu = request.POST.get('nomor_satu')
        nomor_dua = request.POST.get('nomor_dua')
        nomor_tiga = request.POST.get('nomor_tiga')
        nomor_empat = request.POST.get('nomor_empat')
        nomor_lima = request.POST.get('nomor_lima')
        hasil_ujian = int(nomor_satu) + int(nomor_dua) + int(nomor_tiga) + int(nomor_empat) + int(nomor_lima)
        hasil_lulus = False
        if hasil_ujian >= 80:
            hasil_lulus = True
        payload = insert_atlet_nonkualifikasi_ujian_kualifikasi_view(request.session['id'], tahun, batch, tempat, tanggal, hasil_lulus)
        if payload['success']:
            return redirect('tes-kualifikasi:atlet-riwayat-ujian-kualifikasi')
        else:
            messages.info(request, 'Anda tidak dapat mengikuti ujian kualifikasi ini.')
    
    context = {
        'pertanyaan_kualifikasi': form,
    }

    return render(request, 'pertanyaan_kualifikasi.html', context)

def insert_atlet_nonkualifikasi_ujian_kualifikasi_view(id_atlet, tahun, batch, tempat, tanggal, hasil_lulus):
    try:
        cursor = connection.cursor()
        cursor.execute("set search_path to babadu;")
        query = insert_atlet_nonkualifikasi_ujian_kualifikasi_query(id_atlet, tahun, batch, tempat, tanggal, hasil_lulus)
        cursor.execute(query)
    except InternalError as e:
        return {
            'success': False,
        }
    else:
        return {
            'success': True,
        }

def umpire_riwayat_ujian_kualifikasi_view(request):
    if "id" not in request.session or not request.session['is_umpire']:
        return redirect('main:main')
    
    query = umpire_get_riwayat_ujian_kualifikasi_query()
    cursor = connection.cursor()
    cursor.execute("set search_path to babadu;")
    cursor.execute(query)
    res = parse(cursor)
    context = {'riwayat_ujian_kualifikasi': res}
    return render(request, 'riwayat_ujian_kualifikasi.html', context)

def atlet_riwayat_ujian_kualifikasi_view(request):
    if "id" not in request.session or not request.session['is_atlet']:
        return redirect('main:main')
    
    query = atlet_get_riwayat_ujian_kualifikasi_query(request.session['id'])
    cursor = connection.cursor()
    cursor.execute("set search_path to babadu;")
    cursor.execute(query)
    res = parse(cursor)
    context = {'riwayat_ujian_kualifikasi': res}
    return render(request, 'riwayat_ujian_kualifikasi.html', context)
