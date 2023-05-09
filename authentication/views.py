import uuid
import datetime
from django.shortcuts import render, redirect
from authentication.forms import *
from django.db import connection
from base.helper.function import parse

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
            print('invalid')

    context = {'login_form': LoginForm()}
    return render(request, 'login.html', context)

def register(request):
    context = {
        'atlet_form': RegisterAtletForm(),
        'pelatih_form': RegisterPelatihForm(),
        'umpire_form': RegisterUmpireForm(),
    }
    return render(request, 'register.html', context)

def logout(request):
    if "id" in request.session:
        request.session.clear()
        request.session['is_atlet'] = False
        request.session['is_pelatih'] = False
        request.session['is_umpire'] = False
        return redirect('/')
    return redirect('/')
