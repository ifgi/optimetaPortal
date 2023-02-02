#!/bin/sh -e
python manage.py migrate
python manage.py createcachetable
