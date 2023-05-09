import uuid
import datetime
from django.shortcuts import render, redirect
from authentication.forms import *
from django.db import connection
from base.helper.function import parse

session_role_keys = {
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
                print(mem[attr])
                if isinstance(mem[attr], uuid.UUID):
                    request.session[attr] = str(mem[attr])
                elif isinstance(mem[attr], datetime.date):
                    request.session[attr] = mem[attr].strftime('%Y-%m-%d')
                else:
                    request.session[attr] = mem[attr]
            request.session[session_role_keys[mem['member_type']]] = True
            print('session id: ' ,request.session['id'])
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
        return redirect('/')
    return redirect('/')


def is_valid(data):
    return True if len(data) == 1 else False


def is_atlet(id):
    query = f"""
        select * from atlet where id = '{id}';
    """
    cursor = connection.cursor()
    cursor.execute(query)
    res = parse(cursor)
    return True if res else False


def is_pelatih(id):
    query = f"""
        select * from pelatih where id = '{id}';
    """
    cursor = connection.cursor()
    cursor.execute(query)
    res = parse(cursor)
    return True if res else False


def is_umpire(id):
    query = f"""
        select * from umpire where id = '{id}';
    """
    cursor = connection.cursor()
    cursor.execute(query)
    res = parse(cursor)
    return True if res else False
