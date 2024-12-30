from flask import Flask, redirect, url_for, render_template, request, jsonify
import hashlib
from datetime import datetime, timedelta
import jwt
import mysql.connector as connector


# konstanta
SECRET_KEY = "SECRET_KEY"
TOKEN_KEY = "TOKEN_KEY"

# koneksi mysql dengan database
client = connector.connect(
    host="localhost", user="root", passwd="", database="pembayaran_listrik"
)
cursor = client.cursor()


# engine
app = Flask(__name__)


def decoder_cookie(token_receive):
    """
    Decode Cookie
    -------------
    Ini merupakan penerjemah dari cookie\n
    token_receive = str|variabel str

    this is return of data user and role type object\n
    data = {
        'user','role'
    }
    """
    # decode
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
    cursor.execute(
        "SELECT nama, id_level, email FROM account WHERE id LIKE %s", (payload["id"],)
    )
    result = cursor.fetchone()
    data = {
        "user": result[0],
        "role": result[1],
        "email": result[2],
    }
    return data


# tampilkan halaman login


@app.route("/login", methods=["GET"])
def login():
    msg = request.args.get("msg")
    return render_template("login.html", msg=msg)


@app.route("/login/auth", methods=["POST"])
def login_account():
    try:
        email_receive = request.form["email_give"]
        password_receive = request.form["password_give"]
        password_hash = hashlib.sha256((password_receive).encode("utf-8")).hexdigest()
        data = (email_receive, password_hash)
        cursor.execute(
            "SELECT * FROM `account` WHERE `email` LIKE %s AND `password` LIKE %s", data
        )
        hasil = cursor.fetchone()
        print(hasil)
        if hasil:
            payload = {
                "id": hasil[0],
                "username": str(hasil[1]),
                "role": hasil[4],
                "exp": datetime.utcnow() + timedelta(seconds=60 * 60),
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
            return jsonify(
                {
                    "result": "success",
                    "token": token,
                    "token_key": TOKEN_KEY,
                    "msg": "You have logged in!",
                }
            )
        else:
            return jsonify(
                {
                    "result": "failed",
                    "msg": "username dan password tidak ditemukan di database",
                }
            )
    except Exception as e:
        print("error:", e)


# tampilkan halaman register


@app.route("/register", methods=["GET"])
def register():
    return render_template("register.html")


# langkah selanjutnya buat akun


@app.route("/register/auth", methods=["POST"])
def add_account():
    try:
        username_receive = request.form["username_give"]
        email_receive = request.form["email_give"]
        password_receive = request.form["password_give"]
        password_hash = hashlib.sha256((password_receive).encode("utf-8")).hexdigest()

        # carikan nama database
        cursor.execute("SELECT nama,email FROM account WHERE id_level = 2")
        myresult = cursor.fetchall()
        if len(myresult) != 0:
            for x in myresult:
                if x[0] == username_receive and x[1] == email_receive:
                    return jsonify(
                        {"status": "not success", "msg": "username dan email sudah ada"}
                    )
                elif x[1] == email_receive:
                    return jsonify({"status": "not success", "msg": "email sudah ada"})
                elif x[0] == username_receive:
                    return jsonify({"status": "not success", "msg": "nama sudah ada"})
        data = (username_receive, email_receive, password_hash)
        cursor.execute(
            "INSERT INTO `account`(`id`, `nama`, `email`, `password`, `id_level`) VALUES (' ',%s,%s,%s,2)",
            data,
        )
        client.commit()
        if cursor.rowcount:
            return jsonify({"status": "success", "msg": "Successfully registered!"})
        else:
            return jsonify(
                {"status": "not success", "msg": "terdapat kesalahan dalam penambahan"}
            )

    except Exception as e:
        return jsonify({"status": "fail", "msg": "Error: " + str(e)})


# info akun


@app.route("/info_akun", methods=["GET"])
def info_akun():
    nama = request.args.get("nama")
    msg = request.args.get("msg")
    result = request.args.get("result")
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        data1 = decoder_cookie(token_receive)
        cursor.execute(
            "SELECT nama_pelanggan, email, nomor_va, alamat FROM pelanggan WHERE nama_pelanggan LIKE %s",
            (nama,),
        )
        myresult = cursor.fetchone()
        data = {
            "nama": myresult[0],
            "email": myresult[1],
            "no_va": myresult[2],
            "alamat": myresult[3],
        }
        return render_template(
            "info_account.html",
            payloads=data,
            data=data1,
            msg=msg,
            result=result,
            token_key=TOKEN_KEY,
        )
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="Session berakhir,Silahkan Login Kembali"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="Sessin berakhir,Silahkan login kembali!"))


# update info akun


@app.route("/info_akun/update", methods=["POST"])
def update_info_akun():
    try:
        nama = request.form["nama"]
        alamat = request.form["alamat"]
        no_va = request.form["no_va"]

        data = (alamat, int(no_va), nama)
        print(data)
        cursor.execute(
            "UPDATE `pelanggan` SET `alamat`= %s, `nomor_va`= %s WHERE `pelanggan`.`nama_pelanggan` = %s",
            data,
        )
        client.commit()
        print(cursor.rowcount)
        if cursor.rowcount > 0:
            return redirect(
                url_for(
                    "info_akun",
                    result="success",
                    msg="Data berhasil di update",
                    nama=nama,
                )
            )
        else:
            return redirect(
                url_for(
                    "info_akun",
                    result="failed",
                    msg="Terdapat data yang sama",
                    nama=nama,
                )
            )
    except Exception as e:
        return redirect(
            url_for(
                "info_akun",
                result="warning",
                msg="Terjadi kesalahan data : {}".format(e),
                nama=nama,
            )
        )


# landing Page


@app.route("/", methods=["GET"])
def home():
    # ambil cookie
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        data = decoder_cookie(token_receive)
        return render_template("index.html", payloads=data, token_key=TOKEN_KEY)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="Session berakhir,Silahkan Login Kembali"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="Sessin berakhir,Silahkan login kembali!"))


# cek data dan aktivasi user


@app.route("/data_user", methods=["GET"])
def data_user():
    # ambil cookie
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        data = decoder_cookie(token_receive)
        cursor.execute("SELECT * FROM pelanggan")
        result = cursor.fetchall()
        return render_template(
            "data_user.html", users=data, payloads=result, token_key=TOKEN_KEY
        )

    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="Session berakhir,Silahkan Login Kembali"))


# hapus data user


@app.route("/data_user/delete", methods=["POST"])
def delete_data_user():
    try:
        userId = request.form["deleteuserId_receive"]
        cursor.execute("DELETE FROM pelanggan WHERE id_pelanggan = %s", (userId,))
        client.commit()
        print(cursor.rowcount)
        if cursor.rowcount > 0:
            return jsonify(
                {"result": "success", "msg": "data pelanggan berhasil dihapus"}
            )
        else:
            return jsonify(
                {"result": "failed", "msg": "data pelanggan tidak ditemukan"}
            )
    except Exception as e:
        return jsonify({"result": "failed", "msg": str(e)})


# cek tarif dan input tarif


@app.route("/tarif", methods=["GET"])
def tarif():
    # ambil cookie
    msg = request.args.get("msg")
    response = request.args.get("result")
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        data2 = {"msg": msg, "res": response}
        data = decoder_cookie(token_receive)
        cursor.execute("SELECT * FROM tarif")
        result = cursor.fetchall()
        return render_template(
            "tarif.html", payloads=result, users=data, response=data2
        )
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="Session berakhir,Silahkan Login Kembali"))


# hapus tarif


@app.route("/tarif/delete", methods=["POST"])
def delete_tarif():
    try:
        tarifId = request.form["deleteuserId_receive"]
        cursor.execute("DELETE FROM tarif WHERE id_tarif = %s", (tarifId,))
        client.commit()
        # cek berhasil hapus
        if cursor.rowcount > 0:
            return jsonify({"result": "success", "msg": "data tarif berhasil dihapus"})
        else:
            return jsonify({"result": "failed", "msg": "data tarif tidak ditemukan"})
    except Exception as e:
        return jsonify({"result": "failed", "msg": str(e)})


# add tarif


@app.route("/tarif/add", methods=["POST"])
def add_tarif():
    try:
        daya = int(request.form["daya"])
        tarif = request.form["tarif"]
        cursor.execute("SELECT daya FROM tarif")
        myresult = cursor.fetchall()
        if len(myresult) != 0:
            for x in myresult:
                if x[0] == daya:
                    return redirect(
                        url_for(
                            "tarif",
                            msg="Data daya {} sudah ada".format(x[0]),
                            result="failed",
                        )
                    )
        cursor.execute(
            "INSERT INTO `tarif`(`id_tarif`, `daya`, `tarifperkwh`) VALUES (' ',%s,%s)",
            (daya, tarif),
        )
        client.commit()
        if cursor.rowcount > 0:
            return redirect(
                url_for("tarif", msg="Data tarif berhasil disimpan", result="success")
            )
        else:
            return redirect(
                url_for("tarif", msg="Data tarif gagal disimpan", result="success")
            )

    except Exception as e:
        return redirect(
            url_for("tarif", msg="Terjadi kesalahan : {}".format(e), result="failed")
        )


# meteran


@app.route("/meteran", methods=["GET"])
def meteran():
    msg = request.args.get("msg")
    response = request.args.get("result")
    # ambil cookie
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        data2 = {"msg": msg, "res": response}
        data = decoder_cookie(token_receive)
        # cari nama pelanggan
        cursor.execute("SELECT nama_pelanggan FROM pelanggan")
        result = cursor.fetchall()
        payload = {"result": result}
        # ambil penggunaan
        cursor.execute("SELECT * FROM penggunaan")
        result = cursor.fetchall()
        payload["result2"] = result
        return render_template(
            "input_meter.html",
            response=data2,
            payloads=payload,
            users=data,
            token_key=TOKEN_KEY,
        )

    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="Session berakhir,Silahkan Login Kembali"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="Sessin berakhir,Silahkan login kembali!"))


@app.route("/meteran/add", methods=["POST"])
def add_meteran():
    try:
        nama_pelanggan = request.form["nama_pelanggan"]
        bulan = request.form["bulan"]
        tahun = request.form["tahun"]
        tanggal_cek = request.form["tanggal_cek"]
        meteran_awal = request.form["meteran_awal"]
        meteran_akhir = request.form["meteran_akhir"]
        cursor.execute(
            "INSERT INTO `penggunaan`(`id_penggunaan`, `nama_pelanggan`, `tanggal_pengecekan`, `bulan`, `tahun`, `meter_awal`, `meter_akhir`) VALUES (' ',%s,%s,%s,%s,%s,%s)",
            (nama_pelanggan, tanggal_cek, bulan, tahun, meteran_awal, meteran_akhir),
        )
        print(cursor.rowcount)
        cursor.execute("SELECT * FROM tarif ORDER BY daya ASC")
        result = cursor.fetchall()
        cursor.execute("SELECT * FROM tagihan ORDER BY id_tagihan DESC LIMIT 0, 1")
        result2 = cursor.fetchone()
        print(result2)
        for j in result:
            print("a", result2[6], j[1])
            print("b", j[0], result2[0])
            if result2[6] <= j[1]:
                cursor.execute(
                    "UPDATE `tagihan` SET `golongan` = %s WHERE `tagihan`.`id_tagihan` = %s",
                    (j[0], result2[0]),
                )
                break
        print("hati hati")
        client.commit()
        print(cursor.rowcount)
        if cursor.rowcount > 0:
            return redirect(
                url_for("meteran", msg="Data tarif berhasil disimpan", result="success")
            )
        else:
            return redirect(
                url_for("meteran", msg="Data Gagal disimpan", result="fail")
            )
    except Exception as e:
        return redirect(
            url_for(
                "meteran", msg="terjadi kesalahan error {}".format(e), result="fail"
            )
        )


@app.route("/meteran/delete", methods=["POST"])
def delete_meter():
    try:
        meterId = request.form["deleteuserId_receive"]
        cursor.execute("DELETE FROM penggunaan WHERE id_penggunaan = %s", (meterId,))
        client.commit()
        # cek berhasil hapus
        if cursor.rowcount > 0:
            return jsonify({"result": "success", "msg": "data meter berhasil dihapus"})
        else:
            return jsonify({"result": "failed", "msg": "data meter tidak ditemukan"})
    except Exception as e:
        return jsonify({"result": "failed", "msg": str(e)})


# tagihan


@app.route("/tagihan", methods=["GET"])
def tagihan():
    msg = request.args.get("msg")
    response = request.args.get("result")
    # ambil cookie
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        data2 = {"msg": msg, "res": response}
        data = decoder_cookie(token_receive)
        # cari nama pelanggan
        cursor.execute("SELECT * FROM tagihan")

        result = cursor.fetchall()
        payload = {"result": result}
        # gunakan kondisi saat menambah daya
        # cursor.execute('SELECT * FROM ')
        return render_template(
            "tagihan.html",
            response=data2,
            payloads=payload,
            users=data,
            token_key=TOKEN_KEY,
        )

    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="Session berakhir,Silahkan Login Kembali"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="Sessin berakhir,Silahkan login kembali!"))


# status update


@app.route("/tagihan/updateStatus", methods=["POST"])
def status_update_tagihan():
    try:
        name, id_ganti = request.form["nama"], request.form["id"]
        cursor.execute(
            "UPDATE tagihan `status`=%s WHERE id_tagihan==%s", (name, id_ganti)
        )
        print(cursor.rowcount)
    except Exception as err:
        print(err)


# akses lain not found


@app.route("/<path>", methods=["GET"])
def not_found(path):
    return render_template("404.html")


if __name__ == "__main__":
    # DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(host="127.0.0.1", port=5000, debug=True)
