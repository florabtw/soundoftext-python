from flask import Flask, g, render_template, request, send_from_directory
from sounds import controller as c_sounds
from helpers import languages
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', languages=languages.sort_by_value())

@app.route('/sounds', methods=['POST'])
@app.route('/sounds/<idd>', methods=['GET'])
def sounds(idd=None):
    if request.method == 'GET':
        return c_sounds.get_sound(idd)
    elif request.method == 'POST':
        return c_sounds.create()

@app.route('/results', methods=['GET'])
def results():
    if request.method == 'GET':
        return render_template('results.html')

@app.route('/captcha', methods=['POST'])
def captcha():
    if request.method == 'POST':
        return c_sounds.receive_captcha()

@app.route('/static/sounds/<path:filename>', methods=['GET'])
def download_sound(filename):
    return send_from_directory('static/sounds', filename, as_attachment=True)

DATABASE = 'sounds.db'

def connect_db():
    return sqlite3.connect(DATABASE)

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g._database = connect_db()
    return db

@app.before_request
def before_request():
    g.db = get_db()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run()
