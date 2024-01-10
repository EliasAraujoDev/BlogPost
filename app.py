from flask import Flask, redirect, render_template, request, url_for,session
import sqlite3
import os
app = Flask(__name__)



DATABASE =os.path.join(os.path.dirname(__file__), 'Blog.db')

def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor =  conn.cursor()
  

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS blogger(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
    
    cursor.execute('INSERT INTO blogger (username, password) VALUES (?, ?)', ('TaynaraOg', 'Og123'))
    
    conn.commit()
    conn.close()
    print(" Tabela criada com sucesso")

create_table()

app.route('/login')
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM ADM WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            return redirect(url_for('cadastro'))
        else:
            error = "Dados invalidos"
        return render_template('login.html', error=error)

    
    
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
