import uuid
import datetime
from django.shortcuts import render, redirect
from authentication.forms import *
from django.db import connection, InternalError
from base.helper.function import parse
from django.contrib import messages

SESSION_ROLE_KEYS = {
    'atlet': 'is_atlet',
    'pelatih': 'is_pelatih',
    'umpire': 'is_umpire',
}

def login(request):
    if request.method == 'POST':
        nama = request.POST.get('nama')
        email = request.POST.get('email')
        query = f"""
            SELECT
                m.ID,
                m.Nama,
                m.Email,
                COALESCE(u.ID, p.ID, a.ID) AS Member_ID,
                CASE
                    WHEN u.ID IS NOT NULL THEN 'umpire'
                    WHEN p.ID IS NOT NULL THEN 'pelatih'
                    WHEN a.ID IS NOT NULL THEN 'atlet'
                    ELSE 'Unknown'
                END AS Member_Type,
                u.Negara,
                p.Tanggal_Mulai,
                a.Tgl_Lahir,
                a.Negara_Asal,
                a.Play_Right,
                a.Height,
                a.World_Rank,
                a.Jenis_Kelamin
            FROM
                MEMBER m
                LEFT JOIN UMPIRE u ON m.ID = u.ID
                LEFT JOIN PELATIH p ON m.ID = p.ID
                LEFT JOIN ATLET a ON m.ID = a.ID
            WHERE
                m.nama = '{nama}' and m.email = '{email}';
        """
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
                pass
        elif 'umpire_submit' in request.POST:
            umpire_form = RegisterUmpireForm(request.POST)
            if umpire_form.is_valid():
                pass
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
        cursor.execute(f"""
            INSERT INTO
            MEMBER (id, nama, email)
                VALUES
                    (
                        '{id}',
                        '{nama}',
                        '{email}'
                    );
        """)
        cursor.execute(f"""
            INSERT INTO
                ATLET (
                    ID,
                    Tgl_Lahir,
                    Negara_Asal,
                    Play_Right,
                    Height,
                    Jenis_Kelamin
                )
            VALUES
                (
                    '{id}',
                    '{tanggal_lahir}',
                    '{negara}',
                    {play},
                    {tinggi_badan},
                    {jenis_kelamin}
                );
        """)
    except InternalError as e:
        return {
            'success': False,
            'msg': str(e.args)
        }
    else:
        return {
            'success': True,
        }

def logout(request):
    if "id" in request.session:
        request.session.clear()
        request.session['is_atlet'] = False
        request.session['is_pelatih'] = False
        request.session['is_umpire'] = False
        return redirect('/')
    return redirect('/')
