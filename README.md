# Seminario Ciencia de Datos

## First Part

### Install depencendies

- Install conda: https://conda.io/docs/user-guide/install/index.html#

- Install MLflow:

```
pip install mlflow
```

### Get the Code
 
Get the code:
```
git clone https://github.com/anllogui/pythonCI.git
```
There are 3 main folders:
- nb: notebook for training the model
- flaskr: service with the model embedeed
- tests: service testing

### Configure environment

Create environment:
```
conda env create -f environment.yml
conda activate pythonCI
```

### Train the Model
- Run Jupyter
```
cd pythonCI
jupyter notebook
```
- Go to "nb/Simple_Regression.ipynb".
- Execute Notebook

To review the training results:
- Exexute MLFlow ui:
```
cd nb
mlflow ui
```
- go to: http://127.0.0.1:5000

## Second Part

### Automatize

Automatize Model Training and Versioning
```
papermill Simple_Regression.ipynb output.ipynb -p data_ver 1 -p model_ver 1
```

### Expose the model

The service is developed in "pythonCI/flaskr/linreg.py".

To run the service:

**Mac/Linux**:
```
cd ..
export FLASK_APP=flaskr
export FLASK_ENV=development
pip install -e .
flask run
```

**Windows**:
```
cd ..
set "FLASK_APP=flaskr"
set "FLASK_ENV=development"
pip install -e .
flask run
```

To test the service:
```
curl -i -H "Content-Type: application/json" -X POST -d '{"yearsOfExperience":8}' http://localhost:5000/
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

Install Anaconda for all users and give permissions:
sudo addgroup anaconda
sudo chgrp -R anaconda /opt/anaconda3
sudo adduser jenkins anaconda
sudo chmod 777 -R /opt/anaconda3

## Docker 

- Build and run training:
cd training
docker build -t model-training .; docker run --rm --network host model-training


- Build and run execution:
cd training
docker build -t model-exploitation .; docker run --rm --network host model-exploitation


- Delete old images:
docker system prune -a


# Automated Training in Jenkins

#!/bin/bash
echo "---- SETING ENVS ---- "

export PATH=$PATH:/opt/anaconda3/
PYENV_HOME=$WORKSPACE/venv/
export MLFLOW_TRACKING_URI="http://127.0.0.1:5000"



cd training

echo "---- GETING PROPERTIES ----"

file="./train.properties"

if [ -f "$file" ]
then
  echo "$file found."

  while IFS='=' read -r key value
  do
    key=$(echo $key | tr '.' '_')
    eval ${key}=\${value}
  done < "$file"

  echo "Model Version = " ${model_version}
  echo "Data Version  = " ${data_version}
else
  echo "$file not found."
fi

echo "---- CLEANING ENVIRONMENT ----"
if [ -d $PYENV_HOME ]; then
    echo "- Project exists: cleanning.."
    rm -Rf $PYENV_HOME 
fi
source /opt/anaconda3/etc/profile.d/conda.sh
echo "*** creating env ***"
echo $PYENV_HOME
conda env create -f environment.yml --prefix $PYENV_HOME
conda activate $PYENV_HOME
cd nb
papermill simple_regression.ipynb output.ipynb -p data_ver ${data_version} -p model_ver ${model_version}

ls -la ../models

curl -v -u admin:admin -X POST 'http://localhost:8081/service/rest/v1/components?repository=maven-releases' -F "maven2.groupId=models" -F "maven2.artifactId=simple_regresion" -F "maven2.version=${data_version}.${model_version}" -F "maven2.asset1=../models/linear_regression_model_v${model_version}.pkl" -F "maven2.asset1.extension=pkl"