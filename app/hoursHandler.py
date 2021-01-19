from flask import(
    Blueprint, flash, g, redirect, render_template, request, url_for, Response, stream_with_context, current_app
)

from werkzeug.exceptions import abort
from datetime import datetime, timedelta

from app.loginHandler import login_required
from app.databaseHandler import get_db
from app.helper import getTimestamp, getDeltaTimeDecimal
from flask import current_app as app

bp = Blueprint('hours', __name__, url_prefix='/hours')

@bp.route('/checkin')
@login_required
def checkIn():
    db = get_db()

    projects = db.execute(
        'SELECT * FROM project where user_id = ?', (g.user['id'], )
    ).fetchall()

    return render_template('hours/create.html', projects=projects)    

@bp.route('/<int:id>/addManual', methods=('GET', 'POST'))
@login_required
def addManual(id):
    db = get_db()

    if request.method == 'POST':

        start = convertDateTimeLocalToPythonUTC(request.form['starttime'])
        end = convertDateTimeLocalToPythonUTC(request.form['endtime'])
        total_time = getDeltaTimeDecimal(start, end)

        db.execute(
            'INSERT INTO working_hour '
            ' (project_id, user_id, start_time, end_time, total_time, is_finished)'
            ' VALUES (?,?,?,?,?,?)',
            (id, g.user['id'], start, end, total_time, 1)
        )   
        db.commit()  
        return redirect(url_for('landing.dashboard')) 
              
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

@bp.route('/<int:id>/delete', methods=('GET','POST'))
@login_required
def delete(id):
    db = get_db()

    if request.method == 'POST':
        db.execute('DELETE FROM working_hour WHERE id = ?', (id,))
        db.commit()
        return redirect(url_for('landing.dashboard'))

    hours = db.execute(
        'SELECT project.external_id, project.label, working_hour.start_time, working_hour.id FROM project' 
        ' INNER JOIN working_hour ON project.id = working_hour.project_id' 
        ' WHERE project.id = ? AND working_hour.is_finished = ?', 
        (id, 1)
    ).fetchall()

    return render_template('hours/delete.html', hours=hours)

@bp.route('/<int:id>/export.csv', methods=('POST',))
@login_required
def csvExport(id):
    def generate():
        with app.app_context():
            db = get_db()

            query = 'SELECT project.external_id, project.label, working_hour.start_time, working_hour.end_time, working_hour.total_time, working_hour.label FROM project INNER JOIN working_hour ON project.id = working_hour.project_id WHERE project.id = {} AND working_hour.is_finished = {}'.format(id, 1) 

            for row in db.execute(query):
                yield printRow(row)

    return Response(generate(), mimetype='text/csv')

def convertDateTimeLocalToPythonUTC(dtString):
    #Check if String is always formatted that way
    #specifiy tz handling
    year = int(dtString[:4])
    month = int(dtString[5:7])
    day = int(dtString[8:10])
    hour = int(dtString[11:13])
    minute = int(dtString[14:16])

    return datetime(year, month, day, hour, minute)

def printRow(row):
    start = str(row['start_time'])
    end = str(row['end_time'])
    total = str(row['total_time'])
    return (row['external_id'] + ',' + row['label'] + ',' + start + ',' + end + ',' + total + ',' + row['label'] + '\n')
    


