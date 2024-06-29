#!/usr/bin/python3

'''
    Aplication runner.

    To run from flask do:
    flask run

    To run from gunicorn do:
    gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app
'''

from api import appFactory
from dotenv import load_dotenv

load_dotenv('.env')

app = appFactory()
