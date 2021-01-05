"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask, request, render_template
import sys

app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

@app.route('/')
def hello():
    """Renders the landing page."""
    return render_template('index.html')

@app.route('/login')
def renderData():
    """Renders login page"""
    return render_template('login.html')

if __name__ == '__main__':
    import os
    IsSystemOnDocker = os.getenv('ISDOCKER')

    if IsSystemOnDocker:
        HOST = '0.0.0.0'
    else:
        HOST = os.environ.get('SERVER_HOST', 'localhost')

    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555

    app.run(HOST, PORT)
