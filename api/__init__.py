
'''
    Package where endpoints and type validations are made.
'''

from flask import Flask, blueprints

from api.amenities import 
from api.cities import 
from api.countries import 
from api.places import 
from api.reviews import 
from api.users import 

from flasgger import Swagger
from api.swagger import template

def appFactory():
    '''
        Creates an app.
    '''

    app = Flask("HBnB-AlMaWi")

    Swagger(app, template=template)

    return app
