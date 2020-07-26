# set base image (host OS)
FROM continuumio/miniconda3

# set the working directory in the container
WORKDIR /training

# copy the dependencies file to the working directory
COPY training/ .

# install dependencies

RUN conda env create -f environment.yml
# Pull the environment name out of the environment.yml
RUN echo "source activate $(head -1 /tmp/environment.yml | cut -d' ' -f2)" > ~/.bashrc
ENV PATH /opt/conda/envs/$(head -1 /tmp/environment.yml | cut -d' ' -f2)/bin:$PATH

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "pythonCI", "/bin/bash", "-c"]

# command to run on container start
#CMD [ "papermill", "nb/Simple_Regression.ipynb nb/output.ipynb -p data_ver 1 -p model_ver 1" ]
# The code to run when container is started:

ENTRYPOINT conda run -n pythonCI papermill nb/Simple_Regression.ipynb nb/output.ipynb -p data_ver 1 -p model_ver 1