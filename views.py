from flask import Flask, render_template, jsonify, request
from cryptography.fernet import Fernet


def encrypt(message: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(message)


def decrypt(token: bytes, key: bytes) -> bytes:
    return Fernet(key).decrypt(token)


app = Flask(__name__)
app.run(debug=True)

_check = 0

pending_list = {}


@app.route('/')
def qrcode():
    user_name = "sun"
    key = Fernet.generate_key()
    user_encode = encrypt(user_name.encode(), key).decode()
    pending_list[user_name] = {"user_encode": user_encode, "status": False}
    return render_template('qrcode.html', user=user_name, user_code=user_encode)


@app.route('/check-status')
def check():
    global _check
    _check += 1
    print(request.headers['user'], request.headers['user_code'])
    if request.headers['user'] in pending_list:
        if request.headers['user_code'] == pending_list[request.headers['user']]["user_encode"]:
            print(pending_list[request.headers['user']]["status"])
            if pending_list[request.headers['user']]["status"]:
                return jsonify({'status': 'success'})
            else:
                return jsonify({'status': 'pending'})
        else:
            return jsonify({'status': 'wrong token'})
    else:
        return jsonify({'status': 'user not found'})


@app.route('/next')
def next():
    return render_template('next.html')
