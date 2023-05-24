import datetime
import uuid
from event.forms import *
from django.shortcuts import render, redirect
from django.db import InternalError, IntegrityError, connection
from pertandingan.query import *
from pertandingan.forms import *
from base.helper.function import parse
from pertandingan.helper import *

def partai_kompetisi_view(request):
    cursor = connection.cursor()
    cursor.execute("set search_path to babadu;")

    query = get_list_partai_kompetisi_query()
    cursor.execute(query)
    res = parse(cursor)
    list_partai = []
    for partai in res:
        nama_partai = convert_to_slug(f"{partai['nama_event']}/{partai['tahun']}/{partai['jenis_partai']}")
        list_partai.append((nama_partai, (partai), StartPertandinganForm(request.POST or None, prefix=nama_partai)))

    context = {'list_partai': list_partai}

    if request.method == 'POST':
        for partai in list_partai:
            if partai[0] in request.POST and partai[2].is_valid():
                try:
                    query = get_peserta_kompetisi_query(partai[1]['nama_event'], partai[1]['tahun'])
                    cursor.execute(query)
                    res = parse(cursor)
                    jml_peserta = len(res)
                    if jml_peserta % 2 != 0:
                        raise Exception(f'Jumlah peserta tidak genap, count = {jml_peserta}')
                    jenis_babak = get_jenis_babak(jml_peserta)
                    jenis_babak_slug = convert_to_slug(jenis_babak)
                    pertandingan_url = convert_to_slug(partai[0])
                    return redirect(f"/pertandingan/{pertandingan_url}/{jenis_babak_slug}/")
                except Exception as e:
                    raise Exception(e)

    return render(request, 'lihat_partai_kompetisi.html', context)

def pertandingan_view(request, event, tahun, jenis_partai, jenis_babak):
    return render(request, 'babak_pertandingan_view.html')