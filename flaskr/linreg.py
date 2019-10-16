from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

import os
from sklearn.externals import joblib 
import pandas as pd
from sklearn.linear_model import LinearRegression


bp = Blueprint('linreg', __name__, url_prefix='/linreg')

# prediction service
@bp.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            data = request.get_json()
            years_of_experience = [[float(data["yearsOfExperience"])]]
            lin_reg = joblib.load("models/linear_regression_model.pkl")
        except ValueError:
            return jsonify("Please enter a number.")

        return jsonify(lin_reg.predict(years_of_experience).tolist())
        
"""
curl -i -H "Content-Type: application/json" -X POST -d '{"yearsOfExperience":8}' http://localhost:5000/linreg/predict
"""



@bp.route("/info", methods=['GET'])
def current_details():
    if request.method == 'GET':
        try:
            lr = joblib.load("models/linear_regression_model.pkl")

            return jsonify({"coefficients": lr.coef_.tolist(), "intercepts": lr.intercept_})
        except (ValueError, TypeError) as e:
            return jsonify("Error when getting details - {}".format(e))

"""
curl -i -H "Content-Type: application/json" -X GET http://localhost:5000/linreg/info
"""

@bp.route("/retrain", methods=['POST'])
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

            #lin_reg = joblib.load("./linear_regression_model.pkl")
        except ValueError as e:
            return jsonify("Error when retraining - {}".format(e))

        return jsonify("Retrained model successfully.")

@bp.route("/hello", methods=['GET'])
def hello():
    return 1
"""
curl -i -H "Content-Type: application/json" -X GET http://localhost:5000/linreg/hello
"""