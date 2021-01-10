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

    #new users might have no entry. 
    #ToDo: create joins for project data
    try:
        running = db.execute(
            'SELECT project.external_id, project.label, working_hour.id, working_hour.start_time'
            ' FROM working_hour INNER JOIN project ON project.user_id = working_hour.user_id AND'
            ' project.id = working_hour.project_id WHERE working_hour.user_id = ? AND working_hour.is_finished = ?', 
            (user_id, 0)
        ).fetchone()
    except:
        running = None

    try:
        recent = db.execute(
            'SELECT project.external_id, project.label, working_hour.id, working_hour.start_time, working_hour.total_time'
            ' FROM working_hour INNER JOIN project ON project.user_id = working_hour.user_id AND'
            ' project.id = working_hour.project_id WHERE working_hour.user_id = ? AND working_hour.is_finished = ?', 
            (user_id, 1)
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