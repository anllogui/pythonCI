# mlflow tutorial

- Install MLflow:
```
pip install mlflow
```

- Install conda: https://conda.io/docs/user-guide/install/index.html#
- Clone (download) the MLflow repository:
``` 
git clone https://github.com/mlflow/mlflow
```
cd into the examples directory within your clone of MLflow - we’ll use this working directory for running the tutorial. We avoid running directly from our clone of MLflow as doing so would cause the tutorial to use MLflow from source, rather than your PyPi installation of MLflow.

# Train a Model -- cambiado

python examples/sklearn_elasticnet_wine/train.py


# pythonCI

A project example to use CI with Jenkins based on:
https://www.wintellect.com/creating-machine-learning-web-api-flask/

## Code
 
Get the code:
```
git pull https://github.com/anllogui/pythonCI.git
```
There are 3 main folders:
- nb: notebook for training the model
- flaskr: service with the model embedeed
- tests: service testing

## Create the model
Create environment:
```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

To run the notebook:
```
cd nb
jupyter notebook
```
Execute: Simple Regression.ipynb

## Expose the model

The service is developed in "pythonCI/flaskr/linreg.py".

To run the service:
```
export FLASK_APP=flaskr
export FLASK_ENV=development
pip install -e .
flask run
```

To test the service:
```
curl -i -H "Content-Type: application/json" -X POST -d '{"yearsOfExperience":8}' http://localhost:5000/linreg/predict
```

## Continuous integration

After installing Jenkins:
### start
```
brew services start jenkins
```
To access to jenkins: http://localhost:8080

### stop

```
brew services stop jenkins
```

## Shell to Execute

```
echo "---- SETING ENVS ---- "
PYENV_HOME=$WORKSPACE/venv/
export LC_ALL=es_ES.utf-8
export LANG=es_ES.utf-8
export FLASK_APP=$WORKSPACE/flaskr
export FLASK_ENV=development

echo "---- CLEANING ENVIRONMENT ----"
if [ -d $PYENV_HOME ]; then
	echo "- Project exists: cleanning.."
    rm -Rf $PYENV_HOME 
fi
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
pytest
# flask run

```

# Deploy in GCP
https://cloud.google.com/appengine/docs/standard/python/getting-started/python-standard-env
https://cloud.google.com/python/setup