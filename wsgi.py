#!/usr/bin/python3

'''
    Aplication runner.
'''

from api import appFactory

if __name__ == '__main__':
    app = appFactory()
    app.run(host='0.0.0.0')
