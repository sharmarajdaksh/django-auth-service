#!/bin/bash

rm -rf **/migrations/*

/bin/bash -c "python3 manage.py makemigrations"
/bin/bash -c "python3 manage.py migrate"
/bin/bash -c "python3 manage.py test"
/bin/bash -c "python3 manage.py runserver 0.0.0.0:8000"
