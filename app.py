from flask import Flask, flash, render_template, request, url_for, redirect, session
from functools import wraps
import crypto
from datetime import datetime
from db import *
from dotenv import load_dotenv
import queries
import auth

app = Flask(__name__)
load_dotenv(resource_path(".env"))

# Secret Key untuk flash (bisa dipake buat session kalo udah butuh)
app.secret_key = os.getenv("secret_key")


@app.route("/", methods=["GET", "POST"]) #login page
def home():

    username = request.form.get("username")
    password = request.form.get("password")
    
    is_authenticated = auth.dummy_auth(username, password)
    
    if is_authenticated:
            session["username"] = username
            return redirect(url_for("dashboard"))
    elif username is None or password is None:
        return render_template("index.html", page="home")
    else:
        flash("password atau username salah.", "error")
        return render_template("index.html", page="home")


#auth validate
def auth_validate():
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if 'username' in session:
                return f(*args, **kwargs)
            return redirect(url_for("home"))
        return wrapper
    return decorator

@app.route("/dashboard", methods=["GET"]) #dashboard
@auth_validate()
def dashboard():

    

    return render_template("dashboard.html", page="dashboard")


@app.route("/cari_pelanggar", methods=["GET", "POST"]) #cari pelanggar
@auth_validate()
def cari_pelanggar():

    nama_pelanggar = request.form.get("nama_pelanggar")

    if request.method == "POST":
        with engine.connect() as conn:
            pelanggar_list = queries.QueryCariPelanggar(conn, nama_pelanggar)
            NIK = [row[1] for row in pelanggar_list]
            NIK = crypto.decode_string(NIK)
            nama = [row[0] for row in pelanggar_list]

            return render_template("dashboard.html", page="cari_pelanggar", pelanggar=pelanggar_list, nama = nama, NIK = NIK)



    return render_template("dashboard.html", page="cari_pelanggar")


@app.route("/tambah_pelanggaran", methods=["GET","POST"]) #tambah pelanggaran
@auth_validate()
def tambah_pelanggar():

    if request.method == "POST" :
        nama_pelanggar = request.form.get("nama_pelanggar")
        NIK = crypto.encode_string(request.form.get("nik_pelanggar"))
        SIM = crypto.encode_string(request.form.get("no_sim_pelanggar"))
        instansi = request.form.get("instansi_pelanggar")

        with engine.begin() as conn : #insert function
            insertData = queries.QueryInputPelanggar(conn,nama_pelanggar,NIK,SIM,instansi)




    return render_template("form_input_pelanggar.html", page="tambah_pelanggaran")

@app.route("/profil_pelanggar", methods=["GET","POST"]) #profil pelanggar
@auth_validate()
def profil_pelanggar() :


    return render_template("profil_pelanggar.html", page="profil_pelanggar")


if __name__ == "__main__":
    app.run(debug=True)
    
