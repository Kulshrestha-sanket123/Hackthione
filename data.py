from flask import Flask, render_template, request, redirect, flash
import sqlite3
import bcrypt

app = Flask(_name_)
app.secret_key = "secret_key_for_flash_messages"  # Needed for flash messages

# Create database and table if not exist
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match!')
            return redirect('/')

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Insert into database
        try:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (name, email, password)
                VALUES (?, ?, ?)
            ''', (name, email, hashed_password))
            conn.commit()
            conn.close()
            flash('Account created successfully!')
            return redirect('/')
        except sqlite3.IntegrityError:
            flash('Email already exists!')
            return redirect('/')

    return render_template('signup.html')

if _name_ == '_main_':
    app.run(debug=True)