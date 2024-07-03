#!/usr/bin/python3

'''
    Aplication runner.

    To run from flask do:
    flask run

    This will start flask.
    Config for flask is defined in '.flaskenv'


    To run from gunicorn do:
    gunicorn

    This will start multiple workers threads of Flask.
    Config for gunicorn is defined in 'gunicorn.conf.py'
'''

from api import appFactory

app = appFactory()
