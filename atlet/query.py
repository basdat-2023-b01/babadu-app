
def get_all_atlet_kualifikasi_query():
    return f"""
        SELECT
            M.Nama,
            M.Email,
            A.Tgl_Lahir,
            A.Negara_Asal,
            A.Play_Right,
            A.Height,
            A.World_Rank,
            CASE WHEN A.Jenis_Kelamin THEN 'Laki-laki' ELSE 'Perempuan' END AS Jenis_Kelamin,
            AK.World_Tour_Rank,
            COALESCE(SUM(PH.Total_Point), 0) AS Total_Point
        FROM
            MEMBER AS M
            INNER JOIN ATLET AS A ON A.ID = M.ID
            INNER JOIN ATLET_KUALIFIKASI AS AK ON AK.ID_Atlet = A.ID
            LEFT JOIN POINT_HISTORY AS PH ON PH.ID_Atlet = A.ID
        GROUP BY
            M.Nama,
            M.Email,
            A.Tgl_Lahir,
            A.Negara_Asal,
            A.Play_Right,
            A.Height,
            A.World_Rank,
            A.Jenis_Kelamin,
            AK.World_Tour_Rank
        ORDER BY
            A.World_Rank ASC;
    """

def get_all_atlet_nonkualifikasi_query():
    return f"""
        SELECT
            M.Nama,
            M.Email,
            A.Tgl_Lahir,
            A.Negara_Asal,
            A.Play_Right,
            A.Height,
            A.World_Rank,
            CASE WHEN A.Jenis_Kelamin THEN 'Laki-laki' ELSE 'Perempuan' END AS Jenis_Kelamin
        FROM
            MEMBER as M
            INNER JOIN ATLET as A ON A.ID = M.ID
            INNER JOIN ATLET_NON_KUALIFIKASI as AK ON AK.ID_Atlet = A.ID;
    """

def get_all_atlet_ganda_query():
    return f"""
        SELECT
            AG.ID_Atlet_Ganda,
            A1.Nama AS Atlet1_Name,
            A2.Nama AS Atlet2_Name,
            COALESCE(SUM(PH.Total_Point), 0) AS Total_Point
        FROM
            ATLET_GANDA AG
            INNER JOIN MEMBER A1 ON A1.ID = AG.ID_Atlet_Kualifikasi
            INNER JOIN MEMBER A2 ON A2.ID = AG.ID_Atlet_Kualifikasi_2
            LEFT JOIN POINT_HISTORY PH ON PH.ID_Atlet = AG.ID_Atlet_Ganda
        GROUP BY
            AG.ID_Atlet_Ganda,
            A1.Nama,
            A2.Nama;
    """

def get_atlet_pelatih_query(id_pelatih):
    return f"""
        SELECT
            A.ID,
            M.Nama
        FROM
            ATLET AS A
            INNER JOIN MEMBER AS M ON A.ID = M.ID
        WHERE
            A.ID NOT IN (
                SELECT
                    ID_Atlet
                FROM
                    ATLET_PELATIH
                WHERE
                    ID_Pelatih = '{id_pelatih}'
            );
    """

def insert_atlet_pelatih_query(id_atlet, id_pelatih):
    return f"""
        INSERT INTO
            ATLET_PELATIH (ID_Pelatih, ID_Atlet)
                VALUES
                    (
                        '{id_pelatih}',
                        '{id_atlet}'
                    );
    """

def get_atlet_dilatih_query(id_pelatih):
    return f"""
        SELECT
            m.email,
            m.nama,
            a.world_rank
        FROM
            ATLET a
            JOIN MEMBER m ON m.ID = a.ID
            JOIN ATLET_PELATIH ap ON ap.ID_Atlet = a.ID
            JOIN PELATIH p ON p.ID = ap.ID_Pelatih
        WHERE
            p.ID = '{id_pelatih}'
        ORDER BY a.world_rank ASC;
    """