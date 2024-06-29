
'''
    Defines all variables for app.config
'''

from os import environ 

SECRET_KEY = environ.get("SECRET_KEY")
