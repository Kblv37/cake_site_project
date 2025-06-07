from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import os
import sqlite3

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

def init_db():
    with sqlite3.connect('cakes.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS cakes (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            filename TEXT,
                            description TEXT)''')

@app.route('/')
def index():
    with sqlite3.connect('cakes.db') as conn:
        cakes = conn.execute("SELECT filename, description FROM cakes").fetchall()
    return render_template('index.html', cakes=cakes)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        desc = request.form['description']
        if file:
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            with sqlite3.connect('cakes.db') as conn:
                conn.execute("INSERT INTO cakes (filename, description) VALUES (?, ?)", (filename, desc))
            return redirect(url_for('index'))
    return render_template('upload.html')

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    init_db()
    app.run(debug=True)