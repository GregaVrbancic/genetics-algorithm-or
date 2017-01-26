from app import app, socketio
from flask import render_template, send_from_directory
from flask_socketio import emit, disconnect

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/scripts/<path:path>')
def send_js(path):
    return send_from_directory('../client/scripts', path)

@socketio.on('connect', namespace='/io')
def test_connect():
    # need visibility of the global thread object
    print('Client connected')

@socketio.on('my event', namespace='/io')
def test_message(message):
    print('Message received')
    emit('server response', {'data': 'got it!'})
