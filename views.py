from flask import Flask, render_template, jsonify

app = Flask(__name__)
app.run(debug=True)

_check = 0 
@app.route('/')
def qrcode():
    return render_template('qrcode.html')

@app.route('/check-status')
def check():
    global _check   
    _check += 1
    if (_check >= 10):
        _check = 0
        return jsonify({'status': 'success'})
    return jsonify({'status': 'fail'})

@app.route('/next')
def next():
    return render_template('next.html')