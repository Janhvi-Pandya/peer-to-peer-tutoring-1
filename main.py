from flask import Flask, request, render_template, redirect, url_for, session, flash, jsonify
from werkzeug.security import check_password_hash
import sqlite3
import database

app = Flask(__name__)
app.secret_key = 'Cyber@2021'

database.initialize_db()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            with sqlite3.connect('users.db') as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT id, password FROM users WHERE username = ?', (username, ))
                user = cursor.fetchone()

            if user and check_password_hash(user[1], password):
                session['user_id'] = user[0]
                print(f"Login successful for user_id: {user[0]}")
                return redirect(url_for('index'))
            else:
                flash('Invalid username or password')
        except Exception as e:
            print(f"Error during login: {e}")
            flash("An error occurred. Please try again.")
    return render_template('login.html')

@app.route('/index')
def index():
    if 'user_id' not in session:
        flash("You are not logged in.")
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/profiles', methods=['GET'])
def get_profiles():
    with sqlite3.connect('users.db') as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM profiles')

        profiles_data = cursor.fetchall()
        profiles = [dict(row) for row in profiles_data]

    return jsonify(profiles)

@app.route('/saved-videos')
def saved_videos():
    return app.send_static_file('saved-videos.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
