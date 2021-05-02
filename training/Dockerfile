# set base image (host OS)
FROM continuumio/miniconda3 AS environment-image

#RUN set -x && apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
#CMD [ "/bin/bash", "-c" ]
RUN apt-get install -y curl
#RUN conda update -n base -c defaults conda

#RUN useradd --create-home appuser
#USER appuser

ENV PYTHONFAULTHANDLER=1

# set the working directory in the container
#WORKDIR /home/appuser
WORKDIR /

# copy the dependencies file to the working directory
COPY environment.yml .
# install dependencies

RUN conda env create -f environment.yml \
    && conda clean -afy \
    && find /opt/conda/ -follow -type f -name '*.a' -delete \
    && find /opt/conda/ -follow -type f -name '*.pyc' -delete \
    && find /opt/conda/ -follow -type f -name '*.js.map' -delete
    
# DOESN'T WORK --> Pull the environment name out of the environment.yml
#RUN echo "source activate $(head -1 /tmp/environment.yml | cut -d' ' -f2)" > ~/.bashrc
#ENV PATH /opt/conda/envs/$(head -1 /tmp/environment.yml | cut -d' ' -f2)/bin:$PATH
FROM continuumio/miniconda3 AS train-image
COPY --from=environment-image /opt/conda/envs/pythonCI /opt/conda/envs/pythonCI

COPY ./ .

# Pull the environment name out of the environment.yml
RUN echo "conda activate pythonCI" >> ~/.bashrc
ENV PATH /opt/conda/envs/pythonCI/bin:$PATH

# command to run on container start
#CMD [ "papermill", "nb/Simple_Regression.ipynb nb/output.ipynb -p data_ver 1 -p model_ver 1" ]
# The code to run when container is started:

#RUN chmod +x ./train.sh

#CMD ["python", "-c \"import mlflow\""]
#ENTRYPOINT papermill nb/simple_regression.ipynb nb/output.ipynb -p data_ver 1 -p model_ver 1
#ENTRYPOINT ./train.sh
ENTRYPOINT ["/bin/bash", "/train.sh"] 
#ENTRYPOINT ls -la nb
#ENTRYPOINT python -c "import mlflow"
#ENTRYPOINT echo $PATH
#CMD ls -la /opt/conda/envs/pythonCI/bin 

# maintain it running
#CMD tail -f /dev/null
