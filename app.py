from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from flask_mysqldb import MySQL
from os import getenv

app = Flask(__name__)

app.config['MYSQL_HOST'] = getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = getenv('MYSQL_DB')



@app.route('/', methods = ['GET'])
def raiz():
    return render_template('index.html')


@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/contacts')
def contacts():
    return render_template('contactos-usuario.html')

if __name__ == '__main__':
    app.run(debug = True)