# pythonCI

A project example to use CI with Jenkins


# Jenkins Shell

```
echo "---- SETING ENVS ---- "
PYENV_HOME=$WORKSPACE/venv/
export LC_ALL=es_ES.utf-8
export LANG=es_ES.utf-8
export FLASK_APP=$WORKSPACE/flaskr
export FLASK_ENV=development

echo "---- CLEANING ENVIRONMENT ----"
if [ -d $PYENV_HOME ]; then
	echo "- Project exists: cleanning.."
    rm -Rf $PYENV_HOME 
fi
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
pytest
# flask run

```