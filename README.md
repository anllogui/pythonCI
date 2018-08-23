# pythonCI

A project example to use CI with Jenkins


# Jenkins Shell

```
echo "---- SETING ENVS ---- "
PYENV_HOME=$WORKSPACE/.pythonCI/
export LC_ALL=es_ES.utf-8
export LANG=es_ES.utf-8
export FLASK_APP=$WORKSPACE/flaskr
export FLASK_ENV=development
export PATH=$PATH:/Users/anllogui/anaconda3/bin

echo "---- CLEANING ENVIRONMENT ----"
if [ -d $PYENV_HOME ]; then
	echo "- Project exists: cleanning.."
    conda remove -p $PYENV_HOME --all
fi
conda-env create -f environment.yml -p $PYENV_HOME python=3.6
source activate $PYENV_HOME
# conda install --yes --file requirements.txt
pip install -e .
pytest
# flask run

```