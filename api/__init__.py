
'''
    Package where endpoints and type validations are made.
'''

from flask import Flask, blueprints

import api.amenities
import api.countries
import api.users
import api.cities
import api.places
import api.reviews

from flasgger import Swagger
from api.swagger import template


def appFactory():
    '''
        Creates an app.
    '''

    app = Flask("HBnB-AlMaWi")

    app.register_blueprint(api.amenities.bp)
    app.register_blueprint(api.countries.bp)
    app.register_blueprint(api.users.bp)
    app.register_blueprint(api.cities.bp)
    app.register_blueprint(api.places.bp)
    app.register_blueprint(api.reviews.bp)



    Swagger(app, template=template)

    return app
