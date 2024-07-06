#!/usr/bin/python3

'''
    Config for gunicorn.
'''

from os import environ

bind = "0.0.0.0:8000"
workers = 4
wsgi_app = "wsgi:app"

environ['RUNNING_GUNICORN'] = bind
