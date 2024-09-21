from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Datenbankinitialisierung
def init_db():
    with sqlite3.connect('subscribers.db') as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS subscribers (id INTEGER PRIMARY KEY, email TEXT, confirmed INTEGER DEFAULT 0)')
        conn.commit()

# Startseite
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        if email:
            with sqlite3.connect('subscribers.db') as conn:
                conn.execute('INSERT INTO subscribers (email) VALUES (?)', (email,))
                conn.commit()
            flash('Danke für Ihre Anmeldung!', 'success')
            return redirect(url_for('index'))
    return render_template('index.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
