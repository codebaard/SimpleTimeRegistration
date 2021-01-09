from flask import(
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from app.loginHandler import login_required
from app.databaseHandler import get_db

bp = Blueprint('hours', __name__)

@bp.route('/start', methods=('GET', 'POST'))
@login_required
def start():
    if request.method == 'POST':
        project = request.form['project']
        comment = request.form['comment']
        error = None

        # do some errorhandling

        db = get_db()
        # write SQL and update

        return redirect(url_for('landing.dashboard'))
    return render_template('hours/create')

@bp.route('/stop')
@login_required
def stop():
    db = get_db()

    # SQL: find currently running dataset
    # and end it, calculate hours and update dataset.

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
