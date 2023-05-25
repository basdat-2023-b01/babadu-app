import datetime
import uuid
from event.forms import *
from django.shortcuts import render, redirect
from django.db import InternalError, IntegrityError, connection
from pertandingan.query import *
from pertandingan.forms import *
from base.helper.function import parse
from pertandingan.helper import *
import json
import time
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse

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
    cursor = connection.cursor()
    cursor.execute("set search_path to babadu;")

    tahun = 2022
    event = "bala"
    partai = "CD"
    umpire = '0d331503-8696-47cb-9fc5-59d450a781ec'

    cursor.execute("SELECT * FROM partai_peserta_kompetisi WHERE nama_event = %s and jenis_partai = %s and tahun_event = %s", [event, partai, tahun])

    nomer_peserta_kompetisi = cursor.fetchall()
    peserta_kompetisi = []

    for n in nomer_peserta_kompetisi:
        cursor.execute("select * from peserta_kompetisi where nomor_peserta = %s", [n[3]])
        peserta_kompetisi.append(cursor.fetchall())

    peserta_tunggal = []
    peserta_ganda = []

    for n in peserta_kompetisi:
        if n[0][1] == None:
            cursor.execute("select * from member where id = %s", [n[0][2]])
            tunggal = cursor.fetchall()
            peserta_tunggal.append([tunggal[0][0], tunggal [0][1]])
        else:
            cursor.execute("select * from atlet_ganda where \n"
                            "id_atlet_ganda = %s", [n[0][1]])
            ganda = cursor.fetchall()

            cursor.execute("select * from member where id = %s", [ganda[0][1]])
            atlet1 = cursor.fetchall()
            cursor.execute("select * from member where id = %s", [ganda[0][2]])
            atlet2 = cursor.fetchall()

            peserta_ganda.append([ganda[0][0], atlet1[0][0], atlet1[0][1], atlet2[0][0], atlet2[0][1]])

    peserta = []

    for n in peserta_tunggal:
        peserta.append(
            {"id" : n[0],
            "nama" : n[1],
            "tipe" : "tunggal"}
        )
    for n in peserta_ganda:
        peserta.append(
            {"id" : n[0],
            "nama" : n[2] + " & " + n[4],
            "id1" : n[1],
            "id2" : n[3],
            "tipe" : "ganda"}
        )


    JenisBabak = ""
    if len(peserta) == 2:
        JenisBabak = "FINAL"
    elif len(peserta) == 4:
        JenisBabak = "SEMIFINAL"
    elif len(peserta) <= 8:
        JenisBabak = "PEREMPAT FINAL"
    elif len(peserta) <= 16:
        JenisBabak = "R16"
    elif len(peserta) <= 32:
        JenisBabak = "R32"


    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)

    context = {
        "event" : event,
        "partai" : partai,
        "tahun" : tahun,
        "umpire" : umpire,
        "time" : current_time,
        "pertandingan" : [
            {"jenisBabak" : JenisBabak,
                "tim" : []
                },
        ],
    }

    pasangan = []
    count = 0
    for n in peserta:
        if count == 0:
            pasangan.append(n)
            count += 1

        elif count == 1:
            pasangan.append(n)
            context["pertandingan"][0]["tim"].append(pasangan)
            pasangan = []
            count = 0

    return render(request, "babak_pertandingan_view.html", context)