from flask import(
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort
from datetime import datetime, timedelta

from app.loginHandler import login_required
from app.databaseHandler import get_db

bp = Blueprint('hours', __name__, url_prefix='/hours')

@bp.route('/checkin')
@login_required
def checkIn():
    db = get_db()

    projects = db.execute(
        'SELECT * FROM project where user_id = ?', (g.user['id'], )
    ).fetchall()

    return render_template('hours/create.html', projects=projects)    

@bp.route('/<int:project_id>/start', methods=('GET',))
@login_required
def start(project_id):

    db = get_db()

    db.execute(
        'INSERT INTO working_hour (project_id, user_id, state) VALUES (?,?,?)',
        (project_id, g.user['id'], 1)
    )
    db.commit()

    return redirect(url_for('landing.dashboard'))



@bp.route('/<int:id>/stop', methods=('GET',))
@login_required
def stop(id):
    db = get_db()

    timestamp = datetime.now()
    starttime = db.execute(
        'SELECT * FROM working_hour WHERE id = ?', (id, )
    ).fetchone()

    total = timestamp - starttime['started']
    print(total)

    db.execute(
        'UPDATE working_hour SET finished = CURRENT_TIMESTAMP, state = ?, hours_total = ?'
        ' WHERE id = ?',
        (0, str(total), id)
    )
    db.commit()

    return redirect(url_for('landing.dashboard'))

@bp.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_required
def edit(id):
    db = get_db()

    # SQL: find entry and display
    # SQL: update dataset upon POST

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM working_hour WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('landing.dashboard'))
