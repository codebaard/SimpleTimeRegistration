from flask import(
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort
from datetime import datetime, timedelta

from app.loginHandler import login_required
from app.databaseHandler import get_db
from app.helper import getTimestamp, getDeltaTimeDecimal

bp = Blueprint('hours', __name__, url_prefix='/hours')

@bp.route('/checkin')
@login_required
def checkIn():
    db = get_db()

    projects = db.execute(
        'SELECT * FROM project where user_id = ?', (g.user['id'], )
    ).fetchall()

    return render_template('hours/create.html', projects=projects)    

@bp.route('/<int:id>/adddataset', methods=('GET', 'POST'))
@login_required
def addManual(id):
    db = get_db()

    if request.method == 'POST':
        #submit
        print("nothing here yet...")

    project = db.execute(
        'SELECT * FROM project WHERE id = ?', (id, )
    ).fetchone()

    return render_template('hours/manual.html', project=project)

@bp.route('/<int:project_id>/start', methods=('GET',))
@login_required
def start(project_id):

    db = get_db()
    error = None

    running = db.execute(
        'SELECT * FROM working_hour where user_id = ? AND is_finished = ?',
        (g.user['id'], 0)
    ).fetchone()

    if running is None:
        db.execute(
            'INSERT INTO working_hour (project_id, user_id, start_time, label, is_finished) VALUES (?,?,?,?,?)',
            (project_id, g.user['id'], getTimestamp(), 'not set', 0)
        )
        db.commit()
    else:
        error = 'You are still checkedIn at {}. Please checkout first.'.format(running['external_id'] + running['label'])
        flash(error)

    return redirect(url_for('landing.dashboard'))

@bp.route('/<int:id>/stop', methods=('GET',))
@login_required
def stop(id):
    db = get_db()

    end_time = getTimestamp()
    dataset = db.execute(
        'SELECT start_time, label FROM working_hour WHERE id = ?', (id, )
    ).fetchone()

    total_time = getDeltaTimeDecimal(dataset['start_time'], end_time)

    db.execute(
        'UPDATE working_hour SET end_time = ?, total_time = ?, is_finished = ?'
        ' WHERE id = ?',
        (end_time, total_time, 1, id)
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
