
def get_peserta_kompetisi_query(event, tahun):
    return f"""
        (
            SELECT
                pk.Nomor_Peserta,
                ppk.Jenis_Partai
            from
                PESERTA_KOMPETISI pk
                JOIN PARTAI_PESERTA_KOMPETISI ppk ON pk.Nomor_Peserta = ppk.Nomor_Peserta
                AND ppk.nama_event = '{event}'
                AND ppk.tahun_event = {tahun}
        )
        UNION
        (
            SELECT
                pk.Nomor_Peserta,
                ppk.Jenis_Partai
            from
                PESERTA_KOMPETISI pk
                JOIN ATLET_GANDA ag ON pk.ID_Atlet_Ganda = AG.ID_Atlet_Ganda
                JOIN PARTAI_PESERTA_KOMPETISI ppk ON pk.Nomor_Peserta = ppk.Nomor_Peserta
            WHERE
                ppk.nama_event = '{event}'
                AND ppk.tahun_event = {tahun}
        )
        UNION
        (
            SELECT
                pk.Nomor_Peserta,
                ppk.Jenis_Partai
            from
                PESERTA_KOMPETISI pk
                JOIN ATLET_GANDA ag ON pk.ID_Atlet_Ganda = AG.ID_Atlet_Ganda
                JOIN PARTAI_PESERTA_KOMPETISI ppk ON pk.Nomor_Peserta = ppk.Nomor_Peserta
            WHERE
                ppk.nama_event = '{event}'
                AND ppk.tahun_event = {tahun}
        );
    """

def get_list_partai_kompetisi_query():
    return f"""
        SELECT
            e.*,
            pk.Jenis_Partai,
            s.kapasitas
        FROM
            EVENT e
            JOIN STADIUM s ON e.Nama_Stadium = s.Nama
            JOIN PARTAI_KOMPETISI pk ON e.Nama_Event = pk.Nama_Event
            AND e.Tahun = pk.Tahun_Event;
    """