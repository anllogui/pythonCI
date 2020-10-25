# set base image (host OS)
FROM continuumio/miniconda3

#RUN set -x && apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
#CMD [ "/bin/bash", "-c" ]
RUN apt-get install -y curl
RUN conda update -n base -c defaults conda

# set the working directory in the container
WORKDIR /

# copy the dependencies file to the working directory
COPY ./ .

# install dependencies

RUN conda env create -f environment.yml
# DOESN'T WORK --> Pull the environment name out of the environment.yml
#RUN echo "source activate $(head -1 /tmp/environment.yml | cut -d' ' -f2)" > ~/.bashrc
#ENV PATH /opt/conda/envs/$(head -1 /tmp/environment.yml | cut -d' ' -f2)/bin:$PATH

# Pull the environment name out of the environment.yml
RUN echo "conda activate pythonCI" >> ~/.bashrc
ENV PATH /opt/conda/envs/pythonCI/bin:$PATH

# command to run on container start
#CMD [ "papermill", "nb/Simple_Regression.ipynb nb/output.ipynb -p data_ver 1 -p model_ver 1" ]
# The code to run when container is started:

#CMD ["python", "-c \"import mlflow\""]
#ENTRYPOINT papermill nb/simple_regression.ipynb nb/output.ipynb -p data_ver 1 -p model_ver 1
ENTRYPOINT sh train.sh
#ENTRYPOINT ls -la nb
#ENTRYPOINT python -c "import mlflow"
#ENTRYPOINT echo $PATH

# maintain it running
 
CMD tail -f /dev/null