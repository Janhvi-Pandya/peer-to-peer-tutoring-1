import sqlite3
from werkzeug.security import generate_password_hash

DATABASE_PATH = 'users.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS profiles (
                user_id INTEGER,
                university TEXT NOT NULL,
                specialty TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')

        conn.commit()

    if input("Do you want to add sample data? (y/n): ").lower() == 'y':
        add_sample_data()

def add_user(username, password, email):
    with get_db_connection() as conn:
        cursor = conn.cursor()

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        cursor.execute(
            'INSERT INTO users (username, password, email) VALUES (?, ?, ?)',
            (username, hashed_password, email))
        user_id = cursor.lastrowid
        conn.commit()
        return user_id

def add_profile(user_id, university, specialty):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO profiles (user_id, university, specialty) VALUES (?, ?, ?)',
            (user_id, university, specialty))
        conn.commit()

def add_sample_data():
    sample_users = [
        ("user1", "password1", "user1@example.com"),
        ("user2", "password2", "user2@example.com"),
    ]

    sample_profiles = [
        (1, "UVic", "Mathematics"),
        (2, "UVic", "Physics"),
    ]

    try:
        for username, password, email in sample_users:
            user_id = add_user(username, password, email)
            print(f"Added user {username} with ID {user_id}")

        for user_id, university, specialty in sample_profiles:
            add_profile(user_id, university, specialty)
            print(f"Added profile for user ID {user_id}")
    except sqlite3.IntegrityError as e:
        print(f"An error occurred: {e}")

def get_user_by_username(username):
    with get_db_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username, ))
        return cursor.fetchone()

def get_profile_by_userid(user_id):
    with get_db_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM profiles WHERE user_id = ?', (user_id, ))
        return cursor.fetchone()

def get_all_profiles():
    with get_db_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM profiles')
        return [dict(row) for row in cursor.fetchall()]

if __name__ == "__main__":
    initialize_db()
