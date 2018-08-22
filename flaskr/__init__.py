import os
from sklearn.externals import joblib 
import pandas as pd
from sklearn.linear_model import LinearRegression

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

    @app.route("/retrain", methods=['POST'])
    def retrain():
        if request.method == 'POST':
            data = request.get_json()

            try:
                training_set = joblib.load("./training_data.pkl")
                training_labels = joblib.load("./training_labels.pkl")

                df = pd.read_json(data)

                df_training_set = df.drop(["Salary"], axis=1)
                df_training_labels = df["Salary"]

                df_training_set = pd.concat([training_set, df_training_set])
                df_training_labels = pd.concat([training_labels, df_training_labels])

                new_lin_reg = LinearRegression()
                new_lin_reg.fit(df_training_set, df_training_labels)

                os.remove("./linear_regression_model.pkl")
                os.remove("./training_data.pkl")
                os.remove("./training_labels.pkl")

                joblib.dump(new_lin_reg, "linear_regression_model.pkl")
                joblib.dump(df_training_set, "training_data.pkl")
                joblib.dump(df_training_labels, "training_labels.pkl")

                lin_reg = joblib.load("./linear_regression_model.pkl")
            except ValueError as e:
                return jsonify("Error when retraining - {}".format(e))

            return jsonify("Retrained model successfully.")


    @app.route("/currentDetails", methods=['GET'])
    def current_details():
        if request.method == 'GET':
            try:
                lr = joblib.load("./linear_regression_model.pkl")
                training_set = joblib.load("./training_data.pkl")
                labels = joblib.load("./training_labels.pkl")

                return jsonify({"score": lr.score(training_set, labels),
                                "coefficients": lr.coef_.tolist(), "intercepts": lr.intercept_})
            except (ValueError, TypeError) as e:
                return jsonify("Error when getting details - {}".format(e))
                
    return app
