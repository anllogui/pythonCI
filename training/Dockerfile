# set base image (host OS)
FROM continuumio/miniconda3 AS environment-image

RUN conda install mamba -n base -c conda-forge

ENV PYTHONFAULTHANDLER=1

WORKDIR /

# copy the dependencies file to the working directory
COPY environment.yml .
# install dependencies

RUN mamba env update -n base --file environment.yml  \
    && conda clean -afy \
    && find /opt/conda/ -follow -type f -name '*.a' -delete \
    && find /opt/conda/ -follow -type f -name '*.pyc' -delete \
    && find /opt/conda/ -follow -type f -name '*.js.map' -delete


COPY ./ .

ENTRYPOINT ["/bin/bash", "/train.sh"] 
#ENTRYPOINT ls -la nb
#ENTRYPOINT python -c "import mlflow"
#ENTRYPOINT echo $PATH
#CMD ls -la /opt/conda/envs/pythonCI/bin 

# maintain it running
#CMD tail -f /dev/null
