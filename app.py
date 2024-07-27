from flask import Flask, redirect, url_for, render_template, request
import hashlib
import datetime
import mysql.connector as connector

# # koneksi mysql dengan database
# client = connector.connect(
#     host="localhost",
#     user="root",
#     passwd="",
# )
# cursor = client.cursor()

# # buat database
# cursor.execute('CREATE DATABASE IF NOT EXISTS pembayaran_listrik')

# # arahkan ke database
# cursor.execute('USE pembayaran_listrik')

# engine
app = Flask(__name__)

# landing Page


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Handle POST Request here
        return render_template('index.html')
    return render_template('index.html')

# tampilkan halaman login


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

# tampilkan halaman register


@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')

# langkah selanjutnya buat akun


@app.route("/register/auth", methods=['POST'])
def add_account():
    username_receive = request.form['username_give']
    email_receive = request.form['email_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(
        (password_receive).encode('utf-8')).hexdigest()


@app.route("/info_akun", methods=['GET'])
def info_akun():
    return render_template('info_account.html')


@app.route('/data_user', methods=['GET'])
def data_user():
    return render_template('data_user.html')


# akses lain not found


@app.route("/<path>", methods=['GET'])
def not_found(path):
    return render_template('404.html')


if __name__ == '__main__':
    # DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(host='127.0.0.1', port=5000, debug=True)
