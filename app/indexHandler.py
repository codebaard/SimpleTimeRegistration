from flask import(
    Blueprint, flash, g, redirect, render_template, session, request, url_for
)

from werkzeug.exceptions import abort

from app.loginHandler import login_required
from app.databaseHandler import get_db

bp = Blueprint('landing', __name__)

@bp.route('/dashboard')
@login_required
def dashboard():
    user_id = g.user['id']
    db = get_db()

    print(user_id)

    #new users might have no entry. 
    #ToDo: create joins for project data
    try:
        running = db.execute(
            'SELECT * FROM working_hour WHERE user_id = ? AND state = 1', (user_id, )
        ).fetchone()
    except:
        running = None

    try:
        recent = db.execute(
            'SELECT * FROM working_hour WHERE user_id = ? AND state = 0', (user_id, )
        ).fetchall()
    except:
        recent = None

    try:
        projects = db.execute(
            'SELECT * FROM project WHERE user_id = ?', (user_id, )
        ).fetchall()
    except:
        projects = None

    return render_template('indexpage/dashboard.html', running=running, recent=recent, projects=projects)

@bp.route('/authwall')
def authwall():
    return render_template('indexpage/authwall.html')

@bp.route('/')
def index():
    if g.user is None:
        return redirect(url_for('landing.authwall'))
    else:
        return redirect(url_for('landing.dashboard'))