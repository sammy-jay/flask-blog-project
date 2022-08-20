from contextlib import redirect_stderr
import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        db = get_db()
        error = None

        if not username or not password:
            error = "Invalid credentials"
        elif db.execute(
            'SELECT id FROM user WHERE username = ?',(username,)
        ).fetchone() is not None:
            error = "User {} is already registered.".format(username)
        
        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))
        
        flash(error)

    return render_template('auth/register.html')


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?',(username,)
            ).fetchone()
        
        if user is None: 
            error = "Invalid credentials"    
        elif not check_password_hash(user.get('password'), password):
            error = "Invalid credentials"
        
        if error is None:
            session.clear()
            session['user_id'] = user.get('id')
            return redirect(url_for('index'))
        
        flash(error)
        
    return render_template('auth/login.html')