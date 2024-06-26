#!/usr/bin/python3

'''
    Config for gunicorn.
'''

from os import environ
import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
wsgi_app = "wsgi:app"

environ['RUNNING_GUNICORN'] = bind