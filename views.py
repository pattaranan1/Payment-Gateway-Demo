from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def qrcode():
    return render_template('qrcode.html')

@app.route('/next')
def next():
    return render_template('next.html')