from flask import Flask, redirect, url_for, render_template, request, jsonify
import hashlib
from datetime import datetime, timedelta
import jwt
import mysql.connector as connector

# konstanta
SECRET_KEY = 'SECRET_KEY'
TOKEN_KEY = 'TOKEN_KEY'

# koneksi mysql dengan database
client = connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database='Pembayaran_listrik'
)
cursor = client.cursor()


# engine
app = Flask(__name__)

# tampilkan halaman login


@ app.route('/login', methods=['GET'])
def login():
    msg = request.args.get('msg')
    return render_template('login.html')


@ app.route("/login/auth", methods=['POST'])
def login_account():
    try:
        email_receive = request.form['email_give']
        password_receive = request.form['password_give']
        password_hash = hashlib.sha256(
            (password_receive).encode('utf-8')).hexdigest()
        data = (email_receive, password_hash)
        cursor.execute(
            "SELECT * FROM `account` WHERE `email` LIKE %s AND `password` LIKE %s", data)
        hasil = cursor.fetchone()
        if (hasil):
            payload = {
                'id': hasil[0],
                'username': str(hasil[1]),
                'role': hasil[4],
                'exp': datetime.utcnow() + timedelta(seconds=60*60)
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            return jsonify({
                'result': 'success',
                'token': token,
                'token_key': TOKEN_KEY,
                'msg': 'You have logged in!'
            })
        else:
            return jsonify({
                'result': 'failed',
                'msg': 'username dan password tidak ditemukan di database'
            })
    except Exception as e:
        print('error:', e)

# tampilkan halaman register


@ app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')

# langkah selanjutnya buat akun


@ app.route("/register/auth", methods=['POST'])
def add_account():
    try:
        username_receive = request.form['username_give']
        email_receive = request.form['email_give']
        password_receive = request.form['password_give']
        password_hash = hashlib.sha256(
            (password_receive).encode('utf-8')).hexdigest()

        data = (username_receive, email_receive, password_hash)
        cursor.execute(
            "INSERT INTO `account`(`id`, `nama`, `email`, `password`, `id_level`) VALUES (' ',%s,%s,%s,2)", data)
        client.commit()
        return jsonify({
            'status': 'success',
            'msg': 'Successfully registered!'
        })
    except Exception as e:
        return jsonify({'status': 'fail', 'msg': 'Error: '+str(e)})

# info akun


@ app.route("/info_akun", methods=['GET'])
def info_akun():
    return render_template('info_account.html')

# landing Page


@app.route('/', methods=['GET'])
def home():
    # ambil cookie
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        # decode
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        cursor.execute(
            "SELECT nama, id_level FROM account WHERE id LIKE %s", (payload['id'],))
        result = cursor.fetchone()
        data = {
            'user': result[0],
            'role': result[1]
        }
        print(data)
        return render_template('index.html', payloads=data, token_key=TOKEN_KEY)

    except jwt.ExpiredSignatureError:
        return redirect(url_for('login', msg="Session berakhir,Silahkan Login Kembali"))


# cek data dan aktivasi user


@ app.route('/data_user', methods=['GET'])
def data_user():
    # ambil cookie
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        # decode
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        cursor.execute(
            "SELECT nama, id_level FROM account WHERE id LIKE %s", (payload['id'],))
        result = cursor.fetchone()
        print(data)
        return render_template('data_user.html', payloads=data, token_key=TOKEN_KEY)

    except jwt.ExpiredSignatureError:
        return redirect(url_for('login', msg="Session berakhir,Silahkan Login Kembali"))
    # return render_template('data_user.html')

# cek tarif dan input tarif


@ app.route('/tarif', methods=['GET'])
def tarif():
    return render_template('tarif.html')

# meteran


@ app.route('/meteran', methods=['GET'])
def meteran():
    return render_template("input_meter.html")

# tagihan


@ app.route("/tagihan", methods=['GET'])
def tagihan():
    return render_template('tagihan.html')


# akses lain not found


@ app.route("/<path>", methods=['GET'])
def not_found(path):
    return render_template('404.html')


if __name__ == '__main__':
    # DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(host='127.0.0.1', port=5000, debug=True)
