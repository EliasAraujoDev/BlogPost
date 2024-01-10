from flask import Flask, redirect, render_template, request, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'some_secret_key'

DATABASE = os.path.join(os.path.dirname(__file__), 'Blog.db')

def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS blogger(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
    
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS post(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL
            )
        ''')
    
    cursor.execute('INSERT INTO blogger (username, password) VALUES (?, ?)', ('TaynaraOg', 'Og123'))
    
    conn.commit()
    conn.close()
    print("Tabelas criadas com sucesso")

create_table()

@app.route('/')
def index():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM post')
    posts = cursor.fetchall()
    conn.close()
    
    return render_template('index.html', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM blogger WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            return redirect(url_for('criarPost'))
        else:
            error = "Dados inválidos"
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/editPost')
def editPost():
    return render_template('editPost.html')

@app.route('/criarPost', methods=['POST', 'GET'])
def criarPost():
    if request.method == 'POST':
        if 'title' in request.form and 'content' in request.form:
            title = request.form['title']
            content = request.form['content']
            
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO post (title, content) VALUES (?, ?)", (title, content))
            conn.commit()
            conn.close()
            
            return redirect(url_for('index')) 

    return render_template('criarPost.html')  

if __name__ == '__main__':
    app.run(debug=True)
