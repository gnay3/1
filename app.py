"""
Flask web application for a Japanese learning site.

This application implements a simple vocabulary study tool inspired by the
screenshots provided by the user.  It supports user registration (gated by a
purchase code), login and logout functionality, and a dashboard where
registered users can browse and search through a database of more than a
thousand Japanese expressions.  Each expression includes its Japanese form,
romaji reading, translation, part of speech, common collocations, and an
example sentence.  Users can filter expressions by category or search for
terms directly from the dashboard.  Clicking on a vocabulary card reveals
additional details and offers an option to play the pronunciation using the
browser’s built‑in speech synthesis.

Security note:  This application is intended as a demonstration.  In a
production environment you should use proper password hashing (e.g. via
Werkzeug’s `generate_password_hash`), use HTTPS, implement CSRF protection
and integrate a real payment provider.  The purchase code check here is
purely illustrative and should be replaced with a proper order fulfilment
system.
"""

import json
import os
import sqlite3
from functools import wraps

from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    jsonify,
    flash,
)
from werkzeug.security import generate_password_hash, check_password_hash


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'users.db')
VOCAB_PATH = os.path.join(BASE_DIR, 'data', 'vocab.json')


def get_db():
    """Open a new database connection if there is none yet for the
    current application context.
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


def init_db():
    """Initialise the user database if it does not already exist."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )'''
    )
    db.commit()


def login_required(view_func):
    """Decorator that redirects anonymous users to the login page."""

    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return view_func(*args, **kwargs)

    return wrapped_view


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'change-this-secret-key'

    @app.before_request
    def before_request():
        # ensure the database is initialised
        init_db()

    @app.teardown_appcontext
    def close_connection(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

    @app.route('/')
    def index():
        # Redirect to dashboard if logged in, otherwise to login
        if 'user_id' in session:
            return redirect(url_for('dashboard'))
        return redirect(url_for('login'))

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '').strip()
            code = request.form.get('code', '').strip()
            # For demonstration purposes, the purchase code is hardcoded.
            # In a real application this should be validated via your order
            # fulfilment logic (e.g. verifying that the user actually bought
            # access).
            VALID_CODE = 'ACCESS2025'
            if not username or not password or not code:
                flash('Please fill in all fields.', 'danger')
            elif code != VALID_CODE:
                flash('Invalid purchase code. Please enter the correct code from your purchase receipt.', 'danger')
            else:
                db = get_db()
                cursor = db.cursor()
                try:
                    cursor.execute(
                        'INSERT INTO users (username, password) VALUES (?, ?)',
                        (username, generate_password_hash(password))
                    )
                    db.commit()
                except sqlite3.IntegrityError:
                    flash('Username is already taken.', 'danger')
                else:
                    flash('Registration successful. Please log in.', 'success')
                    return redirect(url_for('login'))
        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '').strip()
            db = get_db()
            cursor = db.execute('SELECT id, username, password FROM users WHERE username = ?', (username,))
            user = cursor.fetchone()
            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                session['username'] = user['username']
                return redirect(url_for('dashboard'))
            flash('Invalid username or password.', 'danger')
        return render_template('login.html')

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('login'))

    @app.route('/dashboard')
    @login_required
    def dashboard():
        # Read categories from the vocab file for filtering
        with open(VOCAB_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        categories = sorted({entry.get('category', 'Misc') for entry in data})
        return render_template('dashboard.html', categories=categories)

    @app.route('/api/vocab')
    @login_required
    def api_vocab():
        with open(VOCAB_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)

    return app


if __name__ == '__main__':
    app = create_app()
    # Running the app in debug mode for development; remove debug=True in production.
    app.run(host='0.0.0.0', port=5000, debug=True)