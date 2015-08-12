from flask import Flask, render_template, request
from sounds import controller as c_sounds

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/sounds', methods=['POST'])
def sounds():
    if request.method == 'POST':
        return c_sounds.create()

if __name__ == '__main__':
    app.run(debug=True)
