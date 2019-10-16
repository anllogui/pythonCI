# mlflow tutorial

## First Part

### Install depencendies

- Install MLflow:

```
pip install mlflow
```

- Install conda: https://conda.io/docs/user-guide/install/index.html#

- Clone (download) the MLflow repository:

``` 
git clone https://github.com/mlflow/mlflow
```

### Get the Code
 
Get the code:
```
git pull https://github.com/anllogui/pythonCI.git
```
There are 3 main folders:
- nb: notebook for training the model
- flaskr: service with the model embedeed
- tests: service testing

### Configure environment

Create environment:
```
conda create --name pythonCI
conda activate pythonCI
conda install --file requirements.txt
```

### Train the Model
- Run Jupyter
```
cd pythonCI
jupyter notebook
```
- Go to "nb/Linear Regression.ipynb".
- Execute Notebook

To review the training results:
- Exexute MLFlow ui:
```
mlflow ui
```
- go to: http://127.0.0.1:5000

## Second Part

### Automatize

Automatize Model Training and Versioning
```
papermill Simple\ Regression.ipynb output.ipynb -p data_ver 1 -p model_ver 1
```

### Expose the model

The service is developed in "pythonCI/flaskr/linreg.py".

To run the service:
```
cd ..
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
Install Jenkins for ubuntu:
https://linuxize.com/post/how-to-install-jenkins-on-ubuntu-18-04/

After installing Jenkins:
### start
```
services start jenkins
```
To access to jenkins: http://localhost:8080

### stop

```
service start jenkins
```

## Shell to Execute

```
#!/bin/bash
echo "---- SETING ENVS ---- "
export PATH=$PATH:/Users/anllogui/anaconda3/bin
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
source /Users/anllogui/anaconda3/etc/profile.d/conda.sh
echo "*** creating env ***"
conda create --prefix $PYENV_HOME
echo "*** activate ***"
echo $PYENV_HOME
conda activate $PYENV_HOME
echo "*** install reqs ***"
conda install --file requirements.txt
echo "*** install flask ***"
pip install -e .
pytest
# flask run

```

# Deploy in GCP
https://cloud.google.com/appengine/docs/standard/python/getting-started/python-standard-env
https://cloud.google.com/python/setup