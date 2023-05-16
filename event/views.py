import datetime
from event.forms import *
from django.shortcuts import render, redirect
from django.db import connection
from event.query import *
from base.helper.function import parse
from event.helper import convert_to_slug, convert_to_title

def lihat_event_view(request):
    return render(request, 'lihat_event.html')

def daftar_stadium_view(request):
    if "id" not in request.session:
        return redirect('authentication:login')
    cursor = connection.cursor()
    cursor.execute("set search_path to babadu;")
    query = get_stadium_query()
    cursor.execute(query)
    res = parse(cursor)
    stadium = []
    for item in res:
        item['url'] = convert_to_slug(item['nama'])
        stadium.append(item)
    context = {'list_stadium': stadium}
    
    return render(request, 'daftar_stadium.html', context)

def daftar_event_view(request, stadium):
    stadium = convert_to_title(stadium)
    cursor = connection.cursor()
    cursor.execute("set search_path to babadu;")
    query = get_event_by_stadium_query(stadium)
    cursor.execute(query)
    res = parse(cursor)
    event = []
    for item in res:
        item['url'] = convert_to_slug(item['nama_event']) + f'/{item["tahun"]}'
        for attr in item:
            if isinstance(item[attr], datetime.date):
                date = datetime.datetime.strptime(str(item[attr]), '%Y-%m-%d')
                formatted_date = date.strftime('%d %B %Y')
                item[attr] = formatted_date
        event.append(item)

    context = {'list_event' : event}
            
    return render(request, 'daftar_event.html', context)


def daftar_partai_kompetisi(request, stadium, event, tahun):
    stadium = convert_to_title(stadium)
    event = convert_to_title(event)

    context = {}

    cursor = connection.cursor()
    cursor.execute("set search_path to babadu;")

    query = get_event_detail(event, tahun, stadium)
    cursor.execute(query)
    res = parse(cursor)[0]
    for attr in res:
        if isinstance(res[attr], datetime.date):
            date = datetime.datetime.strptime(str(res[attr]), '%Y-%m-%d')
            formatted_date = date.strftime('%d %B %Y')
            res[attr] = formatted_date
    context = res.copy()

    query = get_partai_kompetisi_by_event_query(event, tahun)
    cursor.execute(query)
    res = parse(cursor)
    partai_kompetisi = []
    for partai in res:
        partai_kompetisi.append(partai['jenis_partai'])
    context['partai_kompetisi'] = partai_kompetisi

    query = get_other_atlet_kualifikasi_query(request.session['id'])
    cursor = connection.cursor()
    cursor.execute("set search_path to babadu;")
    cursor.execute(query)
    res = parse(cursor)
    all_atlet = [(all_atlet['id'], all_atlet['nama']) for all_atlet in res] 
    
    forms = []

    atlet_sex = 'Putra' if request.session['jenis_kelamin'] else 'Putri'

    for partai in partai_kompetisi:
        if 'Ganda' in partai or 'Campuran' in partai:
            form = GandaPartnerForm(all_atlet, request.POST or None, prefix=convert_to_slug(partai))
        else:
            form = TunggalForm(request.POST or None, prefix=convert_to_slug(partai))

        if atlet_sex in partai or 'Campuran' in partai:
            forms.append((partai, form))


    context['forms'] = forms

    if request.method == 'POST':
        for form in forms:
            if form[0] in request.POST and form[1].is_valid():
                print('run')

    return render(request, 'daftar_partai_kompetisi.html', context)

def enrolled_event_view(request):
    return render(request, 'enrolled_event.html')


def pertandingan_view(request, id):
    return render(request, 'pertandingan.html')
