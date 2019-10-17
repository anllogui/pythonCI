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