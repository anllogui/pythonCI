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

## Docker 

- Build and run training:
cd training
docker build -t model-training .; docker run --rm --network host model-training


- Build and run execution:
cd training
docker build -t model-exploitation .; docker run --rm --network host model-exploitation


- Delete old images:
docker system prune -a
