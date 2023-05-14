import datetime
import uuid
from django.shortcuts import render, redirect
from django.db import connection, InternalError
from django.contrib import messages
from base.helper.function import parse
from authentication.forms import *
from authentication.constant import *
from authentication.query import *

def login(request):
    if request.method == 'POST':
        nama = request.POST.get('nama')
        email = request.POST.get('email')
        query = get_user_query(nama, email)
        cursor = connection.cursor()
        cursor.execute("set search_path to babadu;")
        cursor.execute(query)
        res = parse(cursor)
        if len(res) == 1:
            mem = res[0]
            for attr in mem:
                if isinstance(mem[attr], uuid.UUID):
                    request.session[attr] = str(mem[attr])
                elif isinstance(mem[attr], datetime.date):
                    date = datetime.datetime.strptime(str(mem[attr]), '%Y-%m-%d')
                    formatted_date = date.strftime('%d %B %Y')
                    request.session[attr] = formatted_date
                else:
                    request.session[attr] = mem[attr]
            request.session[SESSION_ROLE_KEYS[mem['member_type']]] = True
            return redirect('/dashboard')     
        else:
            messages.info(request,'Username atau Password salah')

    context = {'login_form': LoginForm()}
    return render(request, 'login.html', context)

def register(request):
    if request.method == 'POST':
        if 'atlet_submit' in request.POST:
            atlet_form = RegisterAtletForm(request.POST)
            print(atlet_form.errors)
            if atlet_form.is_valid():
                nama = atlet_form.cleaned_data['nama']
                email = atlet_form.cleaned_data['email']
                negara = atlet_form.cleaned_data['negara']
                tanggal_lahir = atlet_form.cleaned_data['tanggal_lahir']
                play = atlet_form.cleaned_data['play']
                tinggi_badan = atlet_form.cleaned_data['tinggi_badan']
                jenis_kelamin = atlet_form.cleaned_data['jenis_kelamin']
                payload = atlet_register(nama, email, negara, tanggal_lahir, play, tinggi_badan, jenis_kelamin)
                if payload['success']:
                    return redirect('authentication:login')
                else:
                    messages.info(request,payload['msg'])
        elif 'pelatih_submit' in request.POST:
            pelatih_form = RegisterPelatihForm(request.POST)
            if pelatih_form.is_valid():
                nama = pelatih_form.cleaned_data['nama']
                email = pelatih_form.cleaned_data['email']
                kategori = pelatih_form.cleaned_data['kategori']
                tanggal_mulai = pelatih_form.cleaned_data['tanggal_mulai']
                payload = pelatih_register(nama, email, kategori, tanggal_mulai)
                if payload['success']:
                    return redirect('authentication:login')
                else:
                    messages.info(request,payload['msg'])
        elif 'umpire_submit' in request.POST:
            umpire_form = RegisterUmpireForm(request.POST)
            if umpire_form.is_valid():
                print('run 2')
                nama = umpire_form.cleaned_data['nama']
                email = umpire_form.cleaned_data['email']
                negara = umpire_form.cleaned_data['negara']
                print(nama)
                payload = umpire_register(nama, email, negara)
                if payload['success']:
                    return redirect('authentication:login')
                else:
                    messages.info(request,payload['msg'])
    context = {
        'atlet_form': RegisterAtletForm(),
        'pelatih_form': RegisterPelatihForm(),
        'umpire_form': RegisterUmpireForm(),
    }
    return render(request, 'register.html', context)

def atlet_register(nama, email, negara, tanggal_lahir, play, tinggi_badan, jenis_kelamin):
    try:
        id = uuid.uuid4()
        cursor = connection.cursor()
        cursor.execute("set search_path to babadu;")
        mem_query = insert_member_query(id, nama, email)
        cursor.execute(mem_query)
        atlet_query = insert_atlet_query(id, tanggal_lahir, negara, play, tinggi_badan, jenis_kelamin)
        cursor.execute(atlet_query)
    except InternalError as e:
        return {
            'success': False,
            'msg': str(e.args)
        }
    else:
        return {
            'success': True,
        }
    
def pelatih_register(nama, email, kategori, tanggal_mulai):
    try:
        id = uuid.uuid4()
        cursor = connection.cursor()
        cursor.execute("set search_path to babadu;")
        mem_query = insert_member_query(id, nama, email)
        cursor.execute(mem_query)
        pelaih_qeury = insert_pelatih_query(id, tanggal_mulai)
        cursor.execute(pelaih_qeury)
        for k in kategori:
            print(k)
            spesialisasi_kategori_query = insert_pelatih_spesialisasi_query(id, k)
            cursor.execute(spesialisasi_kategori_query)
    except InternalError as e:
        return {
            'success': False,
            'msg': str(e.args)
        }
    else:
        return {
            'success': True,
        }

def umpire_register(nama, email, negara):
    try:
        id = uuid.uuid4()
        cursor = connection.cursor()
        cursor.execute("set search_path to babadu;")
        mem_query = insert_member_query(id, nama, email)
        cursor.execute(mem_query)
        umpire_query = insert_umpire_query(id, negara)
        cursor.execute(umpire_query)
    except InternalError as e:
        return {
            'success': False,
            'msg': str(e.args)
        }
    else:
        return {
            'success': True,
        }
    pass

def logout(request):
    if "id" in request.session:
        request.session.clear()
        request.session['is_atlet'] = False
        request.session['is_pelatih'] = False
        request.session['is_umpire'] = False
        return redirect('/')
    return redirect('/')
