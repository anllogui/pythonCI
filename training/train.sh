#!/bin/bash
echo "---- SETING ENVS ---- "

#export LC_ALL=es_ES.utf-8
#export LANG=es_ES.utf-8
export MLFLOW_TRACKING_URI="http://mlflow_server:5000"

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

echo "---- Launch notebook ----"
cd nb
papermill simple_regression.ipynb output.ipynb -p data_ver ${data_version} -p model_ver ${model_version}
cd ../models
ls -la models
#curl -v -u admin:admin -X POST 'http://localhost:8081/service/rest/v1/components?repository=maven-releases' -F "maven2.groupId=models" -F "maven2.artifactId=simple_regresion" -F "maven2.version=${data_version}.${model_version}" -F "maven2.asset1=../models/linear_regression_model_v${model_version}.pkl" -F "maven2.asset1.extension=pkl"
