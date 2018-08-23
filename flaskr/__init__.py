import os
from flask import (
    Flask, Blueprint, request, session, url_for, jsonify, current_app
)

from logging.config import dictConfig
import logging
from logging.handlers import RotatingFileHandler
from werkzeug.local import LocalProxy


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    handler = RotatingFileHandler('logs/foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        app.logger.info("Hello!")

        return 'Hello, World!'

    from . import linreg
    app.register_blueprint(linreg.bp)
    
    return app
