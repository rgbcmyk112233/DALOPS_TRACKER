import db
import app

def QueryCariPelanggar(conn, nama_pelanggar):
    """
    Mengambil data pelanggar berdasarkan nama pelanggar.

    Args:
        conn: Koneksi database.
        nama_pelanggar (str): Nama pelanggar yang ingin dicari.

    Returns:
        list: Data pelanggar yang sesuai dengan nama yang dicari.
    """

    querycari = db.text("""
        SELECT nama, "NIK"
        FROM profil_pelanggar
        WHERE nama ILIKE :nama_pelanggar
    """)

    return conn.execute(querycari, {"nama_pelanggar": f"%{nama_pelanggar}%"}).fetchall()

def QueryInputPelanggar(conn,nama_pelanggar,nik_pelanggar,no_sim_pelanggar,instansi_pelanggar):
    query = db.text("""
    INSERT INTO profil_pelanggar ("NIK","SIM",nama,instansi)
    VALUES (:nik_pelanggar,:no_sim_pelanggar,:nama_pelanggar,:instansi_pelanggar)
    """)

    return conn.execute(query, 
                        {"nama_pelanggar" : nama_pelanggar,
                         "no_sim_pelanggar" : no_sim_pelanggar,
                         "nik_pelanggar" : nik_pelanggar,
                         "instansi_pelanggar" : instansi_pelanggar})
