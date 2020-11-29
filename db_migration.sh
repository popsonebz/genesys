#!/bin/bash

python manage.py makemigrations 'user_management'
python manage.py migrate
