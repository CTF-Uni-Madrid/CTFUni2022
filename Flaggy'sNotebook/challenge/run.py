import base64
import io
import os
import secrets
import sqlite3

from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)
from PIL import Image
from reportlab.graphics import renderPDF, renderPM
from reportlab.pdfgen import canvas
from svglib.svglib import svg2rlg

from models import User


def init_DB():
    con = sqlite3.connect("data.db", timeout=10)
    cur = con.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS notes(id INTEGER primary key AUTOINCREMENT, title text, content text, userID text)')
    cur.execute(
        'CREATE TABLE IF NOT EXISTS files(id INTEGER primary key AUTOINCREMENT, title text, content text, userID text)')
    cur.execute(
        'CREATE TABLE IF NOT EXISTS users(id INTEGER primary key AUTOINCREMENT, name text UNIQUE, password text)')
    
    con.commit()
    cur.close()


def get_user_by_name(username):
    con = sqlite3.connect("data.db", timeout=10)
    cur = con.cursor()
    query = cur.execute('SELECT * FROM users WHERE name = ?', (username,)).fetchone()
    con.close()

    if query is not None:
        return User(query[0], query[1], query[2])
    else:
        return None
    

def check_password(username, passwd):
    con = sqlite3.connect("data.db", timeout=10)
    cur = con.cursor()
    query = cur.execute('SELECT * FROM users WHERE name = ? AND password = ?', (username,passwd)).fetchone()
    con.close()

    if query is not None:
        return True
    else:
        return False    

    
def get_user_by_id(id):
    # print("ID:", id)
    con = sqlite3.connect("data.db", timeout=10)
    cur = con.cursor()
    query = cur.execute('SELECT * FROM users WHERE id = ?', (id,)).fetchone()
    con.close()

    if query is not None:
        return User(query[0], query[1], query[2])
    else:
        return None    

    
def create_user(username, password):
    
    con = sqlite3.connect("data.db", timeout=10)
    cur = con.cursor()
    query = cur.execute('INSERT INTO users (name, password) VALUES(?, ?)', (username,password)).fetchone()
    query = cur.execute('SELECT * FROM users WHERE name = ? AND password = ?', (username,password)).fetchone()
    
    if query is not None:

        cur.execute(
            'INSERT INTO notes (title, content, userID) VALUES("Test", "Descripcion test", ?)', (query[0],))

        cur.execute(
            'INSERT INTO notes (title, content, userID) VALUES("Notas español 1", "FEAVKAVET@ -> Bienvenid@", ?)', (query[0],))

        cur.execute(
            'INSERT INTO notes (title, content, userID) VALUES("Notas español 2", "AKAVJH -> Evento", ?)', (query[0],))

        cur.execute(
            'INSERT INTO notes (title, content, userID) VALUES("Notas español 3", "WUQBVH -> Humano", ?)', (query[0],))

    
        con.commit()
        con.close()
        return User(query[0], query[1], query[2])
    else:
        con.close()
        return None

app = Flask(__name__)
app.config['SECRET_KEY'] = '4dce525fe32dec7cf32ed21bb376216b7cf6d5ad4069de7aba965f55be0e97cc'
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = "Por favor, logueate para poder continuar."
login_manager.login_message_category = "warning"
login_manager.init_app(app)


@app.route('/')
def main():
    return render_template("index.html")


@login_manager.user_loader
def load_user(user_id):
    # print(user_id)
    return get_user_by_id(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
            return redirect('/')
    
    elif request.method == 'POST':      
        user = request.form.get('username')
        passwd = request.form.get('password')
        
        if user is not None and passwd is not None and check_password(user, passwd):
            userobj = get_user_by_name(user)
            login_user(userobj, remember="True", force="True")
            return redirect("/notas")
        else:
            return render_template("error.html", msg="Login incorrecto.")
            
    else:
        return render_template('login_form.html')


@app.route("/signup", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect('/')
    
    elif request.method == 'POST':
        user = request.form.get('username')
        passwd = request.form.get('password')
        passwd2 = request.form.get('password2')

        if passwd != passwd2:
            return render_template("error.html", msg="Las contraseñas no coinciden.")
        
        if user is not None and passwd is not None:
            userobj = get_user_by_name(user)

            if userobj is not None:
                return render_template("error.html", msg="Ese nombre de usuario ya está siendo utilizado.")
            
            userobj = create_user(user, passwd)
            login_user(userobj, remember="True", force="True")
            return redirect("/")
        else:
            return render_template("error.html", msg="Ha ocurrido un error al registrarte.")
    else:
        return render_template("signup_form.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/notas', methods=['GET', 'POST'])
@login_required
def notes():
    curr_id = current_user.get_id()
    con = sqlite3.connect("data.db", timeout=10)
    cur = con.cursor()

    if request.method == 'POST':

        if request.form['action'] == 'new-note-btn':
            title = request.form.get('titulo')
            desc = request.form.get('descripcion')
            args = (title,desc, curr_id)
            sql = 'INSERT INTO notes (title, content, userID) VALUES(?, ?, ?)'
            query = cur.execute(sql, args)
            con.commit() 
        
        elif request.form['action'] == 'add-content-btn':
            file = request.files['file']
            
            test = cur.execute('SELECT title FROM files WHERE title = ? AND userID = ?',(file.filename,curr_id)).fetchone()

            if test is not None:
                return render_template("error.html", msg="Ya tienes una imagen con ese título")

            if not file.filename.endswith(".svg"):
                return render_template("error.html", msg="¡Flaggy solamente acepta imágenes SVG!")
            
            if not file.content_type.startswith("image/svg"):
                return render_template("error.html", msg="¿Qué estas intentando hacer...?¡Ya te he dicho que Flaggy solamente acepta imágenes SVG!")
            
            title = file.filename
            content = file.read()
            
            args = (title,content,curr_id)
            sql = 'INSERT INTO files (title, content, userID) VALUES(?, ?, ?)'
            query = cur.execute(sql, args)
            con.commit() 
        else:
            return render_template("error.html", msg="Acción no soportada.")

    query = cur.execute('SELECT * FROM notes WHERE userID = ?', (curr_id,)).fetchall()
    con.close()
    return render_template("notas.html", notearray=query)
    


@app.route('/pdfs', methods=['GET', 'POST'])
@login_required
def create_pdf():
    curr_id = current_user.get_id()
    
    con = sqlite3.connect("data.db", timeout=10)
    cur = con.cursor()

    query = cur.execute('SELECT title FROM notes WHERE userID = ?', (curr_id,)).fetchall()
    results = []
    for i in query:
        results.append(i[0])

    query = cur.execute('SELECT title FROM files WHERE userID = ?', (curr_id,)).fetchall()
    all_images = []
    for i in query:
        all_images.append(i[0])    
    
    con.close()    


    if request.method == 'GET':
        return render_template("PDFs.html", options=results, images=all_images)    
    
    elif request.method == 'POST':
        title = request.form.get('note-title')
        img_title = request.form.get('image-title')
        
        if request.form['action'] == 'exportNote':
            var_note = True
            var_img = False
        elif request.form['action'] == 'exportNoteAndImage':
            var_note = True
            var_img = True
        else:
            return render_template("error.html", msg="Acción no soportada.")

        if var_note:
            
            if title not in results:
                return render_template("error.html", msg="Has solicitado una nota que no existe.")
            
            con = sqlite3.connect("data.db", timeout=10)
            cur = con.cursor()
            query = cur.execute('SELECT title, content FROM notes WHERE title = ? AND userID = ?', (title,curr_id)).fetchall()
            pdf_data = []
            for i in query[0]:
                pdf_data.append(i)

            r = secrets.token_hex(16)
            aux = r +'.pdf'
            c = canvas.Canvas(aux)
            c.setFont("Helvetica", 24)
            c.drawString(100, 700, pdf_data[0])
            c.setFont("Helvetica", 16)
            c.drawString(100, 680, pdf_data[1])

            if var_img:
                if img_title not in all_images:
                    return render_template("error.html", msg="Has solicitado una imagen que no existe.")
                
                # retrieve img
                im = cur.execute('SELECT content FROM files WHERE title = ? AND userID = ?', (img_title,curr_id)).fetchall()[0][0].decode()
                
                drawing = svg2rlg(io.BytesIO(im.encode("utf-8")))
                renderPDF.draw(drawing, c, 100, 400)

            c.save()
            con.close()

            f = open(aux, "rb").read()

            base64_pdf = base64.b64encode(f).decode()
            pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="800" height="1000" type="application/pdf">'
            os.remove(aux)
        

            return render_template("render.html", pdf=pdf_display)       

    else:
        return render_template("error.html", msg="El método HTTP no está permitido.")  

@app.route('/calificaciones')
@login_required
def calificaciones():
    return render_template("calificaciones.html")    


# init_DB()
app.run(host='0.0.0.0', debug=False)
