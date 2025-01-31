from flask import Flask, render_template, request, redirect, url_for, flash, json
from dotenv import load_dotenv
from flask_mysqldb import MySQL
from os import getenv
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

app = Flask(__name__)
mysql = MySQL(app)
app.config['MYSQL_HOST'] = getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = getenv('MYSQL_DB')
app.config['SECRET_KEY'] = getenv('SECRET_KEY')

class User(UserMixin):
    def __init__(self, id, nombre, email):
        self.id = id
        self.nombre = nombre
        self.email = email

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, nombre, correo FROM usuarios WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    
    if user:
        return User(user[0], user[1], user[2])  
    return None



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
                clave = generate_password_hash(clave)

                cursor.execute('INSERT INTO usuarios(nombre, correo, clave) VALUES (%s, %s, %s)', (nombre, correo, clave))
                mysql.connection.commit()
                flash('Usuario añadido correctamente', 'success')
        else:
            flash('Debes rellenar todos los campos')
    return render_template('register.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        clave = request.form['clave']
        
        if correo != '' and clave != '':
            cursor = mysql.connection.cursor()
            cursor.execute('use flask_login_contacts_app')
            cursor.execute('select * from usuarios where correo = %s', (correo,))
            usuario = cursor.fetchone()
            if usuario and check_password_hash(usuario[3], clave):
                user_obj = User(usuario[0], usuario[1], usuario[2])
                login_user(user_obj, remember=True)
                return redirect(url_for('contacts'))
            else:
                flash('El usuario no existe')
        else:
            flash('Debes rellenar todos los campos')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('raiz'))


@app.route('/contacts', methods = ['GET', 'POST'])
@login_required
def contacts():
    id = current_user.id
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM contactos WHERE id_usuario = %s', (id,))
    contactos = cursor.fetchall()
    print(contactos)
    lista_contactos = []

    for contacto in contactos:
        lista_contactos.append({'id_contacto':contacto[0] ,'nombre': contacto[1], 'correo': contacto[2], 'telefono':contacto[3]})


    return render_template('contactos-usuario.html', usuario = current_user, contactos = lista_contactos)

@app.route('/añadir-contacto', methods=['GET', 'POST'])
@login_required
def añadir_contacto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        telefono = request.form['telefono']
        id_usuario = current_user.id

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO contactos (nombre, correo, telefono, id_usuario) VALUES (%s, %s, %s, %s)', (nombre, correo, telefono, id_usuario))
        mysql.connection.commit()
        flash('Contacto añadido correctamente')
    return render_template('añadir-contacto.html')
    

@app.route('/delete/<int:id>')
@login_required
def eliminar_contacto(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM contactos WHERE id_contacto = %s',(id,))
    mysql.connection.commit()
    return redirect(url_for('contacts'))

@app.route('/edit/<int:id>', methods = ['GET', 'POST'])
@login_required
def editar_contacto(id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM contactos WHERE id_contacto = %s',(id,))
    contact = cursor.fetchone()
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        telefono = request.form['telefono']
        id_usuario = current_user.id
        cursor.execute('UPDATE contactos SET correo = %s, nombre = %s, telefono = %s WHERE id_contacto = %s',(correo, nombre, telefono, id))
        mysql.connection.commit()
        return redirect(url_for('contacts'))
    return render_template('editar-contacto.html', contacto = {'id':contact[0], 'nombre':contact[1], 'correo':contact[2], 'telefono':contact[3]})

if __name__ == '__main__':
    app.run(debug = True)