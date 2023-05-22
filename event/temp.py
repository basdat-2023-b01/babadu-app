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