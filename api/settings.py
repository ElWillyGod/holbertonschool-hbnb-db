
'''
    Defines all variables for app.config
'''

from os import environ

SECRET_KEY = environ.get("SECRET_KEY")
SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
USE_DATABASE = environ.get("USE_DATABASE")