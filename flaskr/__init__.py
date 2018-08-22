import os
from sklearn.externals import joblib 

from flask import (
    Flask, Blueprint, request, session, url_for, jsonify
)

from logging.config import dictConfig
import logging
from logging.handlers import RotatingFileHandler

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    handler = RotatingFileHandler('logs/foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

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

    # prediction service
    @app.route("/predict", methods=['POST'])
    def predict():
        if request.method == 'POST':
            try:
                data = request.get_json()
                app.logger.info("data: %s", data["yearsOfExperience"])
                years_of_experience = float(data["yearsOfExperience"])
                lin_reg = joblib.load("models/linear_regression_model.pkl")
            except ValueError:
                return jsonify("Please enter a number.")

            return jsonify(lin_reg.predict(years_of_experience).tolist())
            
    from . import api
    app.register_blueprint(api.bp)

    """
    curl -i -H "Content-Type: application/json" -X POST -d '{"yearsOfExperience":8}' http://localhost:5000/predict
    """
    return app
