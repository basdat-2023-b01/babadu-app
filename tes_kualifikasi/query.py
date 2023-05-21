def get_tempat_pelaksanaan_query():
    return f"""
        SELECT tempat FROM UJIAN_KUALIFIKASI;
    """

def get_tanggal_pelaksanaan_query():
    return f"""
        SELECT tanggal FROM UJIAN_KUALIFIKASI;
    """

def get_list_ujian_kualifikasi_query():
    return f"""
        SELECT tahun, batch, tempat, tanggal
        FROM UJIAN_KUALIFIKASI;
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
    """

def trigger_ujian_kualifikasi_query():
    return f"""
        CREATE TRIGGER pernah_mengikuti_ujian 
        BEFORE INSERT OR UPDATE ON atlet_nonkualifikasi_ujian_kualifikasi
        FOR EACH ROW EXECUTE PROCEDURE pernah_mengikuti_ujian();
    """
