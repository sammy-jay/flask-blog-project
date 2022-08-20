from tkinter.messagebox import NO
from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from app.auth import login_required
from app.db import get_db

bp = Blueprint('blog', __name__)

@bp.route("/")
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body,created, author_id, username'
        ' FROM  post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()

    return render_template('blog/index.html', posts=posts)

@bp.route("/create", methods=["GET", "POST"])
def create():
    if request.method == 'POST':
        title = request.form.get("title")
        body = request.form.get("body")
        db = get_db()
        error = None

        if not title or not body:
            error = "Fields are compulsory"

        if error is None:
            author_id = g.user['id']
            if author_id:
                db.execute(
                    'INSERT INTO post (author_id, title, body) VALUES (?, ?, ?)',
                    (author_id, title, body)
                )
                db.commit()
                return redirect(url_for('index'))

        flash(error)

    return render_template('blog/create.html')