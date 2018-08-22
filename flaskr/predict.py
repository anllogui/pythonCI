@bp.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            data = request.get_json()
            years_of_experience = float(data["yearsOfExperience"])
            
            lin_reg = joblib.load("../models/linear_regression_model.pkl")
        except ValueError:
            return jsonify("Please enter a number.")

        return jsonify(lin_reg.predict(years_of_experience).tolist()) 