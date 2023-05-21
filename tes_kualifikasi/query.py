def get_list_ujian_kualifikasi_query():
    return f"""
        SELECT tahun, batch, tempat, tanggal
        FROM UJIAN_KUALIFIKASI;
    """

def umpire_get_riwayat_ujian_kualifikasi_query():
    return f"""
        SELECT
            M.nama, A.tahun, A.batch, A.tempat, A.tanggal,
            CASE
                WHEN A.hasil_lulus = 't' THEN 'Lulus'
                WHEN A.hasil_lulus = 'f' THEN 'Tidak lulus'
            END AS hasil_lulus
        FROM
            MEMBER AS M, ATLET_NONKUALIFIKASI_UJIAN_KUALIFIKASI AS A
        WHERE
            M.id = A.id_atlet;
    """

def atlet_get_riwayat_ujian_kualifikasi_query(id):
    return f"""
        SELECT
            tahun, batch, tempat, tanggal,
            CASE
                WHEN hasil_lulus = 't' THEN 'Lulus'
                WHEN hasil_lulus = 'f' THEN 'Tidak lulus'
            END AS hasil_lulus
        FROM
            ATLET_NONKUALIFIKASI_UJIAN_KUALIFIKASI
        WHERE
            id_atlet = '{id}';
    """

def insert_ujian_kualifikasi_query(tahun, batch, tempat, tanggal):
    return f"""
        INSERT INTO
            UJIAN_KUALIFIKASI (tahun, batch, tempat, tanggal)
                VALUES
                    (
                        '{tahun}',
                        '{batch}',
                        '{tempat}',
                        '{tanggal}'
                    );
    """

def insert_atlet_nonkualifikasi_ujian_kualifikasi_query(id_atlet, tahun, batch, tempat, tanggal, hasil_lulus):
    return f"""
        INSERT INTO
            ATLET_NONKUALIFIKASI_UJIAN_KUALIFIKASI (id_atlet, tahun, batch, tempat, tanggal, hasil_lulus)
                VALUES
                    (
                        '{id_atlet}',
                        '{tahun}',
                        '{batch}',
                        '{tempat}',
                        '{tanggal}',
                        '{hasil_lulus}'
                    );
    """

def stored_procedure_ujian_kualifikasi_query():
    return f"""
        CREATE OR REPLACE FUNCTION pernah_mengikuti_ujian() 
        RETURNS trigger AS 
        $$ 
            BEGIN 
                IF EXISTS 
                    (SELECT * FROM atlet_nonkualifikasi_ujian_kualifikasi 
                    WHERE id_atlet = NEW.id_atlet AND 
                    tahun = NEW.tahun AND 
                    batch = NEW.batch AND 
                    tempat = NEW.tempat AND 
                    tanggal = NEW.tanggal)
                THEN 
                    RAISE EXCEPTION 'error';
                END IF; 
                RETURN NEW;
            END;
        $$ 
        LANGUAGE plpgsql;

        CREATE OR REPLACE FUNCTION hasil_lulus() 
        RETURNS trigger AS 
        $$ 
            BEGIN 
                IF 
                    NEW.hasil_lulus = 't'
                THEN
                    DELETE FROM ATLET_NONKUALIFIKASI_UJIAN_KUALIFIKASI
                        WHERE id_atlet = NEW.id_atlet;
                    INSERT INTO ATLET_KUALIFIKASI (id_atlet, world_rank, world_tour_rank)
                        VALUES (
                            NEW.id_atlet, 
                            (SELECT COUNT(*)+1 FROM ATLET_KUALIFIKASI),
                            (SELECT COUNT(*)+1 FROM ATLET_KUALIFIKASI)
                        );
                    DELETE FROM ATLET_NON_KUALIFIKASI
                        WHERE id_atlet = NEW.id_atlet;
                    INSERT INTO POINT_HISTORY (id_atlet, minggu_ke, bulan, tahun, total_point)
                        SELECT 
                            NEW.id_atlet,
                            EXTRACT(WEEK FROM NEW.tanggal),
                            CASE EXTRACT(MONTH FROM NEW.Tanggal)
                                WHEN 1 THEN 'Januari'
                                WHEN 2 THEN 'Februari'
                                WHEN 3 THEN 'Maret'
                                WHEN 4 THEN 'April'
                                WHEN 5 THEN 'Mei'
                                WHEN 6 THEN 'Juni'
                                WHEN 7 THEN 'Juli'
                                WHEN 8 THEN 'Agustus'
                                WHEN 9 THEN 'September'
                                WHEN 10 THEN 'Oktober'
                                WHEN 11 THEN 'November'
                                WHEN 12 THEN 'Desember'
                            END,
                            EXTRACT(YEAR FROM NEW.tanggal),
                            50;
                END IF; 
                RETURN NEW;
            END;
        $$ 
        LANGUAGE plpgsql;

    """

def trigger_ujian_kualifikasi_query():
    return f"""
        CREATE TRIGGER pernah_mengikuti_ujian 
        BEFORE INSERT OR UPDATE ON atlet_nonkualifikasi_ujian_kualifikasi
        FOR EACH ROW EXECUTE PROCEDURE pernah_mengikuti_ujian();

        CREATE TRIGGER hasil_lulus 
        AFTER INSERT ON atlet_nonkualifikasi_ujian_kualifikasi
        FOR EACH ROW EXECUTE PROCEDURE hasil_lulus();
    """
