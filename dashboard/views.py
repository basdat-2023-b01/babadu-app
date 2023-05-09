from django.shortcuts import render, redirect
from django.db import connection
from base.helper.function import parse

def dashboard_view(request):
    if "id" not in request.session:
        return redirect('authentication:login')
    
    context = {}
    
    if request.session['is_atlet']:
        cursor = connection.cursor()
        cursor.execute("set search_path to babadu;")
        query = f"""
            SELECT
                a.ID,
                k.world_rank,
                k.world_tour_rank,
                CASE
                    WHEN k.ID_Atlet IS NOT NULL THEN 'Qualified'
                    WHEN n.ID_Atlet IS NOT NULL THEN 'Not Qualified'
                END AS status_kualifikasi
            FROM
                ATLET a
                LEFT JOIN ATLET_KUALIFIKASI k ON a.ID = k.ID_Atlet
                LEFT JOIN ATLET_NON_KUALIFIKASI n ON a.ID = n.ID_Atlet
            WHERE
                a.ID = '{request.session['id']}';
        """
        cursor.execute(query)
        res = parse(cursor)[0]
        for attr in res:
            context[attr] = res[attr]
        
        query = f"""
            SELECT
                m.Nama AS nama_pelatih
            FROM
                ATLET_PELATIH ap
                JOIN ATLET a ON a.ID = ap.ID_Atlet
                JOIN PELATIH p ON ap.ID_Pelatih = p.ID
                JOIN MEMBER m ON p.ID = m.ID
            WHERE
                a.ID = '{request.session['id']}';
        """
        cursor.execute(query)
        res = parse(cursor)
        pelatih = []
        for p in res:
            pelatih.append(p['nama_pelatih'])
        pelatih = ', '.join(pelatih)
        context['pelatih'] = pelatih
        if context['status_kualifikasi'] == 'Qualified':
            query = f"""
                SELECT
                    SUM(ph.total_point) AS Total_Points
                FROM
                    POINT_HISTORY ph
                    JOIN ATLET a ON ph.ID_Atlet = a.ID
                WHERE
                    a.ID = '{request.session['id']}';
            """
            cursor.execute(query)
            context['total_point'] = parse(cursor)[0]['total_points']
            
            print('total point: ', res)

    elif request.session['is_pelatih']:
        print('pelatih')
    else:
        print('umpire')

    return render(request, 'dashboard.html', context)
