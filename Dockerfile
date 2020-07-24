Dockerfile

# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /training

# copy the dependencies file to the working directory
COPY training/ .

# install dependencies
RUN conda env create -f environment.yml
RUN conda activate pythonCI

# command to run on container start
CMD [ "papermill", "nb/Simple_Regression.ipynb nb/output.ipynb -p data_ver 1 
-p model_ver 1" ]