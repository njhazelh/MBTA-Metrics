#!/bin/bash

ENV_NAME='mbta-env'

echo 'Creating environment' $ENV_NAME 

python -m venv --without-pip mbta-env
source mbta-env/bin/activate
# TODO - find a better workaround for broken pyvenv
curl https://bootstrap.pypa.io/get-pip.py | python
deactivate

echo 'Environment' $ENV_NAME 'created.'
