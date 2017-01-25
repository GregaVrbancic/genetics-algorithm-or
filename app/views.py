from app import app
from flask import render_template, send_from_directory

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/scripts/<path:path>')
def send_js(path):
    return send_from_directory('../client/scripts', path)