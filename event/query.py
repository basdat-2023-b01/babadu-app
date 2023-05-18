
def get_stadium_query():
    return f"""
        SELECT * FROM STADIUM;
    """

def get_stadium_detail_query(nama):
    return f"""
        SELECT * FROM STADIUM WHERE NAMA = '{nama}'
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

def get_partai_peserta_kompetisi_reg_query(event, tahun):
    return f"""
        SELECT
            CASE
                WHEN PK.Jenis_Partai = 'MS' THEN 'Tunggal Putra'
                WHEN PK.Jenis_Partai = 'WS' THEN 'Tunggal Putri'
                WHEN PK.Jenis_Partai = 'MD' THEN 'Ganda Putra'
                WHEN PK.Jenis_Partai = 'WD' THEN 'Ganda Putri'
                WHEN PK.Jenis_Partai = 'XD' THEN 'Ganda Campuran'
            END AS jenis_partai,
            COUNT(PPK.jenis_partai) AS jumlah_pendaftar
        FROM

            EVENT as E
            JOIN PARTAI_KOMPETISI as PK ON E.Nama_Event = PK.Nama_Event AND E.Tahun = PK.Tahun_Event
            LEFT JOIN PARTAI_PESERTA_KOMPETISI as PPK ON PPK.Nama_Event = PK.Nama_Event 
                AND PPK.Tahun_Event = PK.Tahun_Event 
                AND PK.Jenis_Partai = PPK.Jenis_Partai
            WHERE E.Nama_Event = '{event}' AND E.Tahun = {tahun}
        GROUP BY PK.jenis_partai;
    """

def get_other_atlet_kualifikasi_diff_gender_query(id, jenis_kelamin):
    return f"""
        SELECT
            *
        FROM
            ATLET_KUALIFIKASI as AK
            JOIN MEMBER as M ON AK.ID_Atlet = M.ID
            JOIN ATLET as A ON A.ID = AK.ID_Atlet
        WHERE
            AK.ID_Atlet != '{id}' and A.Jenis_Kelamin != {jenis_kelamin}
            AND AK.ID_Atlet NOT IN (
                SELECT
                    AG.ID_Atlet_Kualifikasi
                FROM
                    ATLET_GANDA as AG
            )
            AND AK.ID_Atlet NOT IN (
                SELECT
                    AG.ID_Atlet_Kualifikasi_2
                FROM
                    ATLET_GANDA as AG
            );
    """

def get_other_atlet_kualifikasi_same_gender_query(id, jenis_kelamin):
    return f"""
        SELECT
            *
        FROM
            ATLET_KUALIFIKASI as AK
            JOIN MEMBER as M ON AK.ID_Atlet = M.ID
            JOIN ATLET as A ON A.ID = AK.ID_Atlet
        WHERE
            AK.ID_Atlet != '{id}' and A.Jenis_Kelamin = {jenis_kelamin}
            AND AK.ID_Atlet NOT IN (
                SELECT
                    AG.ID_Atlet_Kualifikasi
                FROM
                    ATLET_GANDA as AG
            )
            AND AK.ID_Atlet NOT IN (
                SELECT
                    AG.ID_Atlet_Kualifikasi_2
                FROM
                    ATLET_GANDA as AG
            );
    """

def get_world_tour_rank_query(id):
    return f"""
        SELECT world_tour_rank FROM ATLET_KUALIFIKASI WHERE ID_Atlet = '{id}';
    """

def insert_peserta_kompetisi_tunggal_query(id_atlet_kualifikasi, world_rank, world_tour_rank):
    return f"""
        INSERT INTO
            PESERTA_KOMPETISI (ID_Atlet_Kualifikasi, World_Rank, World_Tour_Rank)
        SELECT
            '{id_atlet_kualifikasi}',
            {world_rank},
            {world_tour_rank}
        WHERE
            NOT EXISTS (
                SELECT
                    1
                FROM
                    PESERTA_KOMPETISI
                WHERE
                    ID_Atlet_Kualifikasi = '{id_atlet_kualifikasi}'
            );
        SELECT
            Nomor_Peserta
        FROM
            PESERTA_KOMPETISI WHERE id_atlet_kualifikasi = '{id_atlet_kualifikasi}';
    """

def insert_and_get_atlet_ganda(id, id_atlet_1, id_atlet_2):
    return f"""
        INSERT INTO
            ATLET_GANDA (
                ID_Atlet_Ganda,
                ID_Atlet_Kualifikasi,
                ID_Atlet_Kualifikasi_2
            )
        SELECT
            '{id}',
            '{id_atlet_1}',
            '{id_atlet_2}'
        WHERE
            NOT EXISTS (
                SELECT
                    1
                FROM
                    ATLET_GANDA
                WHERE
                    (ID_Atlet_Kualifikasi = '{id_atlet_1}'
                    AND ID_Atlet_Kualifikasi_2 = '{id_atlet_2}')
                    OR
                    (ID_Atlet_Kualifikasi = '{id_atlet_2}'
                    AND ID_Atlet_Kualifikasi_2 = '{id_atlet_1}')
            );

        SELECT
            *
        FROM
            ATLET_GANDA
        WHERE
            (ID_Atlet_Kualifikasi = '{id_atlet_1}'
            AND ID_Atlet_Kualifikasi_2 = '{id_atlet_2}') 
            OR (
            ID_Atlet_Kualifikasi = '{id_atlet_2}'
            AND ID_Atlet_Kualifikasi_2 = '{id_atlet_1}'
        );
    """

def insert_peserta_kompetisi_ganda_query(id_atlet_ganda, world_rank, world_tour_rank):
    return f"""
        INSERT INTO
            PESERTA_KOMPETISI (
                ID_Atlet_Ganda,
                World_Rank,
                World_Tour_Rank
            )
        SELECT
            '{id_atlet_ganda}',
            {world_rank},
            {world_tour_rank}
        WHERE
            NOT EXISTS (
                SELECT
                    1
                FROM
                    PESERTA_KOMPETISI
                WHERE
                    ID_Atlet_Ganda = '{id_atlet_ganda}'
        );
        SELECT
            Nomor_Peserta
        FROM
            PESERTA_KOMPETISI WHERE id_atlet_ganda = '{id_atlet_ganda}';
    """

def insert_partai_peserta_kompetisi_query(jenis_partai, nama_event, tahun_tahun, nomor_peserta):
    return f"""
    INSERT INTO
        PARTAI_PESERTA_KOMPETISI (
            Jenis_Partai,
            Nama_Event,
            Tahun_Event,
            Nomor_Peserta
        )
    VALUES ('{jenis_partai}', '{nama_event}', {tahun_tahun}, {nomor_peserta});
    """
