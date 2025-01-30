from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from flask_mysqldb import MySQL
from os import getenv

load_dotenv()

app = Flask(__name__)
mysql = MySQL(app)
app.config['MYSQL_HOST'] = getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = getenv('MYSQL_DB')
app.config['SECRET_KEY'] = getenv('SECRET_KEY')



@app.route('/', methods = ['GET'])
def raiz():
    return render_template('index.html')


@app.route('/register', methods = ['GET', 'POST'])
def register():
    cursor = mysql.connection.cursor()
    cursor.execute('use flask_login_contacts_app')
    cursor.execute('select * from usuarios')
    usuarios = cursor.fetchall()
    correos = []
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        clave = request.form['clave']
        
        if nombre != '' and correo != '' and clave != '':

            for usuario in usuarios:
                correos.append(usuario[2])
                


            if correo in correos:
                flash('El usuario ya existe', 'error')
            else:
                correos.append(correo)
                cursor.execute('INSERT INTO usuarios(nombre, correo, clave) VALUES (%s, %s, %s)', (nombre, correo, clave))
                mysql.connection.commit()
                flash('Usuario añadido correctamente', 'success')
        else:
            flash('Debes rellenar todos los campos')
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/contacts')
def contacts():
    return render_template('contactos-usuario.html')

if __name__ == '__main__':
    app.run(debug = True)