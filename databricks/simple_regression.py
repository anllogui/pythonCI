# Databricks notebook source
# MAGIC %md
# MAGIC # Simple Linear Regression
# MAGIC 
# MAGIC [Linear regression](https://en.wikipedia.org/wiki/Linear_regression) is perhaps the most simple of all of the models. Do you remember the linear formula where `m` is the slope and `b` is where the line starts on the y-axis?
# MAGIC 
# MAGIC $$y=mx+b$$
# MAGIC 
# MAGIC This is a simple linear model since there is only one coefficient - `mx`.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Imports and load data

# COMMAND ----------

# MAGIC %pip install mlflow

# COMMAND ----------

import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import mlflow
import mlflow.sklearn
sns.set()
%matplotlib inline

# COMMAND ----------

data_ver = 2
model_ver = 2
mlflow.start_run() 

# COMMAND ----------

mlflow.log_param("data_ver", data_ver)
mlflow.log_param("model_ver", model_ver)

df = pd.read_csv("../data/SalaryData%s.csv" % data_ver)

# COMMAND ----------

df.head()

# COMMAND ----------

df.shape
df.drop(["Name"], axis = 1, inplace=True)

# COMMAND ----------

# MAGIC %md
# MAGIC Before continuing, check if there are any missing data in the data set.

# COMMAND ----------

df.isnull().values.any()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Split data
# MAGIC 
# MAGIC Splitting the depedent variable (`Salary`) out from the indepedent variable (`YearsExperience`) so we can build our model.
# MAGIC 
# MAGIC We use the `train_test_split` method from `scikit-learn` to split our data. The `test_size` is used to tell it what percentage of the data to use for our testing data set and the `random_state` is used as a seed for the random splitting of the data. The seed will randomize the split in the same way each time for reproducability.

# COMMAND ----------

train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)
df_copy = train_set.copy()
df_copy.head()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Exploratory Data Analysis
# MAGIC 
# MAGIC Explore the data to find trends. Using the `describe` method to get descriptive statistics on numerical columns of our data. The `corr` method to calculate correlations between the columns of our data. And plotting with `matplotlib` via the `plot` method to get a visual of the data. Also using `seaborn`'s `regplot` to give us what a linear regression line of our data may look like and to verify that our data looks linear.

# COMMAND ----------

df_copy.describe()

# COMMAND ----------

df_copy.corr()

# COMMAND ----------

df_copy.plot.scatter(x='YearsExperience', y='Salary')

# COMMAND ----------

# Regression plot
sns.regplot('YearsExperience', # Horizontal axis
           'Salary', # Vertical axis
           data=df_copy)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Train
# MAGIC 
# MAGIC We're making three other data sets for the `LinearRegression` model:
# MAGIC - `test_set` that is just the `YearsExperience` column (dropping the `Salary` column) that will be used for analyzing and scoring our model.
# MAGIC - `train_labels` that is just the `Salary` column to train the `LinearRegression` model what the answers are when passing in the years of experience input.
# MAGIC - `train_set` that is also just the `YearsExperience` column (dropping the `Salary` column) that will be passed into the `LinearRegression`'s `fit` method as the `x` parameter.

# COMMAND ----------

test_set_full = test_set.copy()

test_set = test_set.drop(["Salary"], axis=1)

# COMMAND ----------

test_set.head()

# COMMAND ----------

train_labels = train_set["Salary"]
train_set_full = train_set.copy()
train_set = train_set.drop(["Salary"], axis=1)
train_set.head()

# COMMAND ----------

# MAGIC %md
# MAGIC Now that we have our data in the correct form, we pass in the `train_set` and `train_labels` into the `fit` method to train the model.

# COMMAND ----------

lin_reg = LinearRegression()

lin_reg.fit(train_set, train_labels)

# COMMAND ----------

# MAGIC %md
# MAGIC Now we have a model and can call the `predict` function on it with inputs. 

# COMMAND ----------

salary_pred = lin_reg.predict(test_set)
salary_pred

# COMMAND ----------

# MAGIC %md
# MAGIC ## Analyze Results

# COMMAND ----------

# MAGIC %md
# MAGIC We can get the coefficients and intercept from our model.

# COMMAND ----------

print("Coefficients: ", lin_reg.coef_)
print("Intercept: ", lin_reg.intercept_)

mlflow.log_metric("coef", float(lin_reg.coef_))
mlflow.log_metric("intercept", float(lin_reg.intercept_))

# COMMAND ----------

# MAGIC %md
# MAGIC With that information we can build our line formula - $y=9423.81532303x + 25321.5830118$
# MAGIC 
# MAGIC We can compare our predictions to our testing set label columns.

# COMMAND ----------

print(salary_pred)
print(test_set_full["Salary"])

# COMMAND ----------

# MAGIC %md
# MAGIC Models in `scikit-learn` have a `score` method. Depending on the model, this method will do a different calculation. For `LinearRegression` it calculates the $r^2$.

# COMMAND ----------

lin_reg.score(test_set, test_set_full["Salary"])

# COMMAND ----------

# MAGIC %md
# MAGIC There's also a separate `r2_score` method that will calculate the $r^2$.

# COMMAND ----------

score = r2_score(test_set_full["Salary"], salary_pred)
mlflow.log_metric("score", score)
print(score)


# COMMAND ----------

# MAGIC %md
# MAGIC We can also plot our test data as a scatter plot and, with our predicted salary that we got from our model, plot a line to see how well it fits the data.

# COMMAND ----------

plt.scatter(test_set_full["YearsExperience"], test_set_full["Salary"], color='blue')
plt.plot(test_set_full["YearsExperience"], salary_pred, color='red', linewidth=2)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Export 

# COMMAND ----------

mlflow.sklearn.log_model(lin_reg, "linear_regression_master")
mlflow.end_run()
