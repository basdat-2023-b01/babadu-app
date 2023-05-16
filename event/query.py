
def get_stadium_query():
    return f"""
        SELECT * FROM STADIUM;
    """

def get_event_by_stadium_query(stadium):
    return f"""
        SELECT
            *
        FROM
            EVENT
        WHERE
            nama_stadium = '{stadium}';
    """

def get_event_detail(event, tahun, stadium):
    return f"""
        SELECT
            e.nama_event,
            e.tahun,
            e.negara,
            e.tgl_mulai,
            e.tgl_selesai,
            e.kategori_superseries,
            e.total_hadiah,
            s.nama as nama_stadium,
            s.kapasitas
        FROM EVENT as e
            JOIN STADIUM as s on e.nama_stadium = s.nama
        WHERE
            nama_stadium = '{stadium}' AND
            nama_event = '{event}' AND
            tahun = {tahun}
            ;
    """

def get_partai_kompetisi_by_event_query(event, tahun):
    return f"""
        SELECT
            CASE
                WHEN PK.Jenis_Partai = 'MS' THEN 'Tunggal Putra'
                WHEN PK.Jenis_Partai = 'WS' THEN 'Tunggal Putri'
                WHEN PK.Jenis_Partai = 'MD' THEN 'Ganda Putra'
                WHEN PK.Jenis_Partai = 'WD' THEN 'Ganda Putri'
                WHEN PK.Jenis_Partai = 'XD' THEN 'Ganda Campuran'
            END AS jenis_partai
        FROM
            EVENT as e
            JOIN PARTAI_KOMPETISI as pk ON e.nama_event = pk.nama_event
            and e.tahun = pk.tahun_event
        WHERE
            e.nama_event = '{event}'
            AND e.tahun = {tahun};
    """

def get_other_atlet_kualifikasi_query(id):
    return f"""
        SELECT
        *
        FROM
            ATLET_KUALIFIKASI AK
            JOIN MEMBER M ON AK.ID_Atlet = M.ID
        WHERE
            AK.ID_Atlet != '{id}';
    """

def get_other_atlet_kualifikasi_gender_query(id, jenis_kelamin):
    return f"""
        SELECT
        *
        FROM
            ATLET_KUALIFIKASI AK
            JOIN MEMBER M ON AK.ID_Atlet = M.ID
            JOIN ATLET A ON A.ID = AK.ID_Atlet
        WHERE
            AK.ID_Atlet != '{id}' AND A.Jenis_kelamin = {jenis_kelamin};
    """