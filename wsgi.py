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


    To run from docker use:
    docker-compose up -d
    This will run all containers.
'''
from dotenv import load_dotenv
from api import appFactory

load_dotenv(".env", verbose=True)

app = appFactory()
