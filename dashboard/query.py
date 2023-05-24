

def get_atlet_detail_query(id):
    return f"""
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
            a.ID = '{id}';
    """

def get_atlet_pelatih_detail_query(id):
    return f"""
        SELECT
            m.Nama AS nama_pelatih
        FROM
            ATLET_PELATIH ap
            JOIN ATLET a ON a.ID = ap.ID_Atlet
            JOIN PELATIH p ON ap.ID_Pelatih = p.ID
            JOIN MEMBER m ON p.ID = m.ID
        WHERE
            a.ID = '{id}';
    """

def get_atlet_kualifikasi_detail_query(id):
    return f"""
        SELECT
            SUM(ph.total_point) AS Total_Points
        FROM
            POINT_HISTORY ph
            JOIN ATLET a ON ph.ID_Atlet = a.ID
        WHERE
            a.ID = '{id}';
    """

def get_pelatih_spesialisasi_detail_query(id):
    return f"""
        SELECT
            s.Spesialisasi
        FROM
            PELATIH_SPESIALISASI ps
            JOIN SPESIALISASI s ON ps.ID_Spesialisasi = s.ID
        WHERE
            ps.ID_Pelatih = '{id}';
    """

def get_umpire_detail_query(id):
    pass