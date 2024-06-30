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
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv('.env')

app = appFactory()

####################################################################################################
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+mysqldb://root:@localhost/hbnb'
app.config['USE_DATABASE'] = True
db = SQLAlchemy(app)
