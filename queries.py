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
        SELECT *
        FROM profil_pelanggar
        WHERE nama ILIKE :nama_pelanggar OR "NIK" ILIKE :nama_pelanggar
    """)

    return conn.execute(querycari, {"nama_pelanggar": f"%{nama_pelanggar}%"}).fetchall()
