from flask import(
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from app.loginHandler import login_required
from app.databaseHandler import get_db

bp = Blueprint('projects', __name__)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        label = request.form['label']
        number = request.form['number']

        try:
            parent_id = request.form['parent_id']
        except:
            parent_id = None

        error = None

        if not label:
            error = 'A projectname is required.'

        if not number:
            error = 'A projectnumber is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO project'
                ' (external_id, label, parent_id, user_id, role_id)'
                ' VALUES (?,?,?,?,?)',
                (number, label, parent_id, g.user['id'], 1)
            )
            db.commit()

        return redirect(url_for('landing.dashboard'))
    return render_template('projects/create.html')

@bp.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_required
def edit(id):
    db = get_db()

    if request.method == 'POST':

        newLabel = request.form['label']
        newExternal_id = request.form['number']

        db.execute(
            'UPDATE project SET label = ?, external_id = ? WHERE id = ?',
            (newLabel, newExternal_id, id, )
        )
        db.commit()

        return redirect(url_for('landing.dashboard'))

    project = db.execute(
        'SELECT * FROM project where id = ?', (id, )
    ).fetchone()

    return render_template('projects/update.html', project=project)

@bp.route('/<int:id>/export')
@login_required
def export(id):

    db = get_db()
    summary = 0
    
    hours = db.execute(
        'SELECT project.external_id, project.label, working_hour.total_time FROM project' 
        ' INNER JOIN working_hour ON project.id = working_hour.project_id' 
        ' WHERE project.id = ? AND working_hour.is_finished = ?', 
        (id, 1)
    ).fetchall()

    for h in hours:
        summary += h['total_time']

    return render_template('projects/export.html', hours=hours, summary=summary)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM project WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('landing.dashboard'))
