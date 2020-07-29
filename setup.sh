#!/usr/bin/env bash

python3 -m pip install virtualenv

virtualenv venv

source venv/bin/activate

pip install -r requirements.txt

deactivate
