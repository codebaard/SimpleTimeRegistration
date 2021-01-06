"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask, request, render_template
import sys
import os

def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
    )

    # Make the WSGI interface available at the top level so wfastcgi can get it.
    #wsgi_app = app.wsgi_app

    if test_config is None:
        #load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    #ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def hello():
        """Renders the landing page."""
        return render_template('login.html')

    @app.route('/webapp')
    def renderData():
        """Renders main menu"""
        return render_template('index.html')

    @app.errorhandler(404)
    def handle_404(e):
        # handle all other routes here
        #return send_from_directory('.','404.html')    
        return  render_template('404.html')

    from . import databaseHandler as db
    db.init_app(app)

    return app        

"""     if __name__ == '__main__':
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

        app.run(HOST, PORT) """
