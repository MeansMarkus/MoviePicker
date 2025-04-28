from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
#Secret key for session management (Security)
app.secret_key = "markus_is_coding_fire"

def get_db():
    """
    New database connection to users.db

    :return: SQLite3 connection with row factory
    :rtype: sqlite3.Connection
    """
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """
    Redirect to login page

    :return: Redirect response
    """
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    User registration form and submission

    :return: Registration template or redirect on success
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        try:
            db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            db.commit()
            return redirect('/login')
        except:
            return "Username already taken!"
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login form and auth

    :return: Redirect to recommendations or back to login on failure
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password)).fetchone()
        if user:
            session['user_id'] = user['id']
            session['username'] = username
            return redirect('/recommendations')
        else:
            return "Invalid credentials!"
    return render_template('login.html')

@app.route('/recommendations')
def recommendations():
    """
    Display recommendations page for logged-in user

    :return: Recommendations template/redirect to login
    """
    if 'user_id' not in session:
        return redirect('/login')
    username = session['username']
    # TODO: Add recommendation logic later
    return render_template('recommendations.html', username=username)

@app.route('/logout')
def logout():
    """
    Log user out by clearing session

    :return: Redirect to login page
    """
    session.clear()
    return redirect('/login')
