#Last modified: 2022-08-07
import hmac
from flask import Flask, render_template, request, session
import mysql.connector as mariadb
import os
import logging
import logging.handlers
from face_recog import recognize
import hashlib
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

app = Flask(__name__)
mariadb_connect = mariadb.connect(host='127.0.0.1',port=3306,user='root', password='tom', database='seokwon')
logging.basicConfig(filename="log.txt", filemode="w", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
#key = b'LM\xe5\xb3\xb2\x95T~r?\xef@7\x99\x01\x04/xq\x1c\xbb6\x9d\x01N\xe0\xe3\xbb\xd9\xe9\xb1k'
import ctypes

def msgbox(title, text):
  return ctypes.windll.user32.MessageBoxW(0, text, title, 0x00001000 | 0x00000010)

def login_err():
  msgbox('Login failed', "Enter valid username and password.")
  return home()

def register_err():
  msgbox('Register failed', "Enter valid username and password")
  return home()

def register_id_err():
  msgbox('Register failed', "Username already exists")
  return home()

@app.route('/')
def home():
  if not session.get('logged_in'):
    return render_template('login.html')
  else:
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def do_login():
  login = request.form
  input_id = login['username']
  input_pw = login['password']
  if input_id=="" or input_pw=="":
    return login_err()
  else:
    logger = logging.getLogger(input_id)
    logger.info("The user %s logged in", input_id)
  cur = mariadb_connect.cursor()
  qry = 'SELECT * FROM test WHERE id="{0}"'.format(input_id)
  cur.execute(qry)
  db_row = cur.fetchone()
  #print("db_row: ", db_row)
  if db_row==None: return login_err() #exception handling
  db_pw = db_row[1]
  if check_password_hash(db_pw, input_pw):
    session['logged_in'] = True
  elif db_pw!=input_pw:
    return login_err()

  return home()
  #input_pw_hash = hashlib.pbkdf2_hmac('sha256',input_pw.encode('utf-8'),key,100000)
  #input_pw_hash_hex = input_pw_hash.hex()
  #if hmac.compare_digest(db_pw, input_pw_hash_hex):
    #session['logged_in'] = True
  #elif db_pw != input_pw_hash_hex:
    #return login_err()
  #return home()

@app.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'GET':
    return render_template("signup.html")
  else:
    id = request.form['username']
    pw = request.form['password']
    email = request.form['email']
    name = request.form['name']
    if id == "" or pw == "" or email == "" or name == "": return register_err()
    hash_pw = generate_password_hash(pw, "sha256")
    #encoding = pw.encode('utf-8')
    #digest = hashlib.pbkdf2_hmac('sha256', encoding, key, 100000)
    #hex_hash = digest.hex()
    cur = mariadb_connect.cursor()
    qry = "INSERT INTO test (ID, Password, Email, Name) VALUES ('%s','%s','%s', '%s')" % (id,hash_pw,email,name)
    #qry = "INSERT INTO test (ID, Password, Email, Name) VALUES ('%s','%s','%s', '%s')" % (id,hex_hash,email,name)
    cur.execute(qry)
    mariadb_connect.commit()
    logger = logging.getLogger(id)
    logger.info("The user %s registered", id)
  return home()

@app.route('/logout')
def logout():
  session['logged_in'] = False
  logging.info('Current user logged out')
  return home()

@app.route('/task')
def task():
  recognize()
  return home()

if __name__ == "__main__":
  app.secret_key = os.urandom(12)
  app.run(debug=False,host='0.0.0.0', port=5000)