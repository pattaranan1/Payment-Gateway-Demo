from flask import Flask, render_template, jsonify, request
from cryptography.fernet import Fernet
from datetime import datetime, timedelta
from flask_socketio import SocketIO, emit
import time


def encrypt(message: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(message)


def decrypt(token: bytes, key: bytes) -> bytes:
    return Fernet(key).decrypt(token)


pending_list = {}


def background_thread(user=""):
    global pending_list
    while True:
        try:
            socketio.emit(
                'status', {'payment_status': pending_list[user]["status"]})
        except KeyError:
            print("data was not ready")
        time.sleep(3)


app = Flask(__name__)
app.run(debug=True)
socketio = SocketIO(app)

_check = 0
thread = None
current_user = None


@app.route('/')
def qrcode():
    user_name = "sun"
    key = Fernet.generate_key()
    user_encode = encrypt(user_name.encode(), key).decode()
    pending_list[user_name] = {"user_encode": user_encode,
                               "status": False, "time_stamp": datetime.now()}
    return render_template('qrcode.html', user=user_name, user_code=user_encode)


@app.route('/check-status')
def check():
    global _check
    _check += 1
    if request.headers['user'] in pending_list:
        if request.headers['user_code'] == pending_list[request.headers['user']]["user_encode"] and pending_list[request.headers['user']]["time_stamp"] + timedelta(seconds=180) > datetime.now():
            if pending_list[request.headers['user']]["status"]:
                del pending_list[request.headers['user']]
                return jsonify({'status': 'success'})
            else:
                return jsonify({'status': 'pending'})
        else:
            return jsonify({'status': 'wrong token or token time out'})
    else:
        return jsonify({'status': 'user not found'})


@app.route('/active-token')
def active_token():
    if request.headers['user'] in pending_list:
        pending_list[request.headers['user']]["status"] = True
        return jsonify({'status': 'True'})
    else:
        return jsonify({'status': 'user not found'})


@app.route('/next')
def next():
    return render_template('next.html')


@socketio.on('connect')
def connect(data):
    print("connected")


@socketio.on('my event')
def handle_my_custom_event(json):
    global thread
    if thread is None:
        thread = socketio.start_background_task(
            target=background_thread, user=json['current_user'])
