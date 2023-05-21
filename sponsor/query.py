def daftar_sponsor_query(id):
    return f"""
        SELECT id, nama_brand
        FROM SPONSOR
        WHERE id NOT IN (
            SELECT S.id
            FROM SPONSOR AS S, ATLET_SPONSOR AS A
            WHERE '{id}' = A.id_atlet AND
            S.id = A.id_sponsor
        );
    """

def insert_atlet_sponsor_query(id_atlet, id_sponsor, tgl_mulai, tgl_selesai):
    return f"""
        INSERT INTO
            ATLET_SPONSOR (id_atlet, id_sponsor, tgl_mulai, tgl_selesai)
                VALUES
                    (
                        '{id_atlet}',
                        '{id_sponsor}',
                        '{tgl_mulai}',
                        '{tgl_selesai}'
                    );
    """

def get_list_sponsor_query(id):
    return f"""
        SELECT S.nama_brand, A.tgl_mulai, A.tgl_selesai
        FROM SPONSOR AS S, ATLET_SPONSOR AS A
        WHERE id_atlet = '{id}' AND
        S.id = A.id_sponsor;
    """