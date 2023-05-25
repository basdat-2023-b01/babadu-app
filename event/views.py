import datetime
import re
import uuid
from event.forms import *
from django.shortcuts import render, redirect
from django.db import InternalError, connection
from event.query import *
from base.helper.function import parse
from event.helper import convert_to_slug, convert_to_title
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

def lihat_event_view(request):
    if "id" not in request.session or not request.session['is_atlet']:
        return redirect('main:main')
    return render(request, 'lihat_event.html')

def daftar_stadium_view(request):
    if "id" not in request.session or not request.session['is_atlet']:
        return redirect('main:main')
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
    if "id" not in request.session or not request.session['is_atlet']:
        return redirect('main:main')
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

@csrf_exempt
def daftar_partai_kompetisi(request, stadium, event, tahun):
    if "id" not in request.session or not request.session['is_atlet']:
        return redirect('main:main')
    stadium = convert_to_title(stadium)
    event = convert_to_title(event)

    context = {}
    cursor = connection.cursor()
    cursor.execute("set search_path to babadu;")

    query = get_stadium_detail_query(stadium)
    cursor.execute(query)
    res = parse(cursor)[0]
    context['kapasitas'] = res['kapasitas']

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
    partai_kompetisi = [partai['jenis_partai'] for partai in res]
    context['partai_kompetisi'] = partai_kompetisi

    query = get_other_atlet_kualifikasi_diff_gender_query(request.session['id'], request.session['jenis_kelamin'], event, tahun)
    cursor.execute(query)
    res = parse(cursor)
    atlet_difference_gender = [(atlet_difference_gender['id'], atlet_difference_gender['nama']) for atlet_difference_gender in res] 

    query = get_other_atlet_kualifikasi_same_gender_query(request.session['id'], request.session['jenis_kelamin'], event, tahun)
    cursor.execute(query)
    res = parse(cursor)
    atlet_same_gender = [(atlet_same_gender['id'], atlet_same_gender['nama']) for atlet_same_gender in res] 

    query = get_partai_peserta_kompetisi_reg_query(event, tahun)
    cursor.execute(query)
    res = parse(cursor)
    jumlah_pendaftar ={}
    for partai in res:
        jumlah_pendaftar[partai['jenis_partai']] = partai['jumlah_pendaftar']
    forms = []

    atlet_sex = 'Putra' if request.session['jenis_kelamin'] else 'Putri'

    for partai in partai_kompetisi:
        if 'Campuran' in partai:
            form = GandaPartnerForm(atlet_difference_gender, request.POST or None, prefix=convert_to_slug(partai))
        elif 'Ganda' in partai:
            form = GandaPartnerForm(atlet_same_gender, request.POST or None, prefix=convert_to_slug(partai))
        elif 'Tunggal' in partai:
            form = TunggalForm(request.POST or None, prefix=convert_to_slug(partai))
        else:
            continue

        if atlet_sex in partai or 'Campuran' in partai:
            forms.append((partai, form, jumlah_pendaftar[partai]))

    context['forms'] = forms

    if request.method == 'POST':
        query = get_world_tour_rank_query(request.session['id'])
        cursor.execute(query)
        world_tour_rank = parse(cursor)[0]['world_tour_rank']
        for form in forms:
            if form[0] in request.POST and form[1].is_valid():
                try:
                    if 'Tunggal' in form[0]:
                        query = insert_peserta_kompetisi_tunggal_query(
                            request.session['id'],
                            request.session['world_rank'],
                            world_tour_rank
                        )
                        cursor.execute(query)
                        nomor_peserta = parse(cursor)[0]['nomor_peserta']
                        if 'Putra' in form[0]:
                            query = insert_partai_peserta_kompetisi_query('MS', event, tahun, nomor_peserta)
                        else:
                            query = insert_partai_peserta_kompetisi_query('WS', event, tahun, nomor_peserta)
                        cursor.execute(query)
                    else:
                        id = uuid.uuid4()
                        id_atlet_2 = form[1].cleaned_data['daftar_atlet']
                        query = insert_and_get_atlet_ganda(id, request.session['id'], id_atlet_2) 
                        cursor.execute(query)
                        id_atlet_ganda = parse(cursor)[0]['id_atlet_ganda']
                        query = insert_peserta_kompetisi_ganda_query(
                            id_atlet_ganda,
                            request.session['world_rank'],
                            world_tour_rank
                        )
                        cursor.execute(query)
                        res = parse(cursor);
                        nomor_peserta = res[0]['nomor_peserta']
                        if 'Putra' in form[0]:
                            query = insert_partai_peserta_kompetisi_query('MD', event, tahun, nomor_peserta)
                        elif 'Putri' in form[0]:
                            query = insert_partai_peserta_kompetisi_query('WD', event, tahun, nomor_peserta)
                        else:
                            query = insert_partai_peserta_kompetisi_query('XD', event, tahun, nomor_peserta)
                        cursor.execute(query)
                except Exception as e:
                    if e is InternalError:
                        trimmed_string = re.sub(r'\(|\)|\'', '', str(e.args))
                        message = re.search(r'\[([^]]+)\]', trimmed_string).group(1)
                        messages.info(request, message)
                    else:
                        pass
                else:
                    return redirect(request.META['HTTP_REFERER'])

    return render(request, 'daftar_partai_kompetisi.html', context)

def enrolled_partai_kompetisi_event_view(request):
    if "id" not in request.session or not request.session['is_atlet']:
        return redirect('main:main')
    cursor = connection.cursor()
    cursor.execute("set search_path to babadu;")
    query = get_enrolled_partai_kompetisi_event(request.session['id'])
    cursor.execute(query)
    res = parse(cursor)
    context = {'events': res}
    return render(request, 'enrolled_partai_kompetisi_event.html', context)

@csrf_exempt
def enrolled_event_view(request):
    if "id" not in request.session or not request.session['is_atlet']:
        return redirect('main:main')
    cursor = connection.cursor()
    cursor.execute("set search_path to babadu;")
    query = get_enrolled_event_query(request.session['id'])
    cursor.execute(query)
    res = parse(cursor)
    events = []
    for event in res:
        form = UnenrollEventForm(request.POST or None, prefix=convert_to_slug(''))
        events.append((event, form))

    if request.method == 'POST':
        for event in events:
            if f"{event[0]['nama_event']}-{event[0]['tahun']}" in request.POST and event[1].is_valid():
                try:
                    event_detail = event[0]
                    query = get_partai_peserta_kompetisi_by_event_query(request.session['id'], event_detail['nama_event'], event_detail['tahun'])
                    cursor.execute(query)
                    res = parse(cursor)
                    nomor_peserta = [no['nomor_peserta'] for no in res]
                    for nomor in nomor_peserta:
                        query = unenroll_event_query(nomor, event_detail['nama_event'], event_detail['tahun'])
                        cursor.execute(query)
                except InternalError as e:
                    print(e)
                    raise Exception(e)
                else:
                    return redirect(request.META['HTTP_REFERER'])

    context = {'events': events}
    return render(request, 'enrolled_event.html', context)
