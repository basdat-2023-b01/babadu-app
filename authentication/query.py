
def get_user_query(nama, email):
    return f"""
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

def insert_member_query(id, nama, email):
    return f"""
        INSERT INTO
        MEMBER (id, nama, email)
            VALUES
                (
                    '{id}',
                    '{nama}',
                    '{email}'
                );
        """

def insert_atlet_query(id, tanggal_lahir, negara, play, tinggi_badan, jenis_kelamin):
    return f"""
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
    """

def insert_pelatih_query(id, tanggal_mulai):
    return f"""
        INSERT INTO
        PELATIH (ID, Tanggal_Mulai)
        VALUES
            (
                '{id}',
                '{tanggal_mulai}'
            );
    """

def insert_umpire_query(id, negara):
    return f"""
        INSERT INTO
        UMPIRE (ID, Negara)
        VALUES
            (
                '{id}',
                '{negara}'
            );
    """

def insert_pelatih_spesialisasi_query(pelatih_id, kategori):
    return f"""
        INSERT INTO PELATIH_SPESIALISASI (ID_Pelatih, ID_Spesialisasi)
        SELECT 
            '{pelatih_id}', 
            ID FROM SPESIALISASI 
        WHERE Spesialisasi = '{kategori}';
    """