
'''
    Package where endpoints and type validations are made.
'''

from flask import Flask

from blueprints import *

import api.jwt

from flasgger import Swagger
from api.swagger import template


def appFactory():
    '''
        Creates an app.
    '''

    app = Flask("HBnB-AlMaWi")

    app.register_blueprint(amenities.bp)
    app.register_blueprint(countries.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(cities.bp)
    app.register_blueprint(places.bp)
    app.register_blueprint(reviews.bp)

    app.config['JWT_SECRET_KEY'] = '00Ba3EpLas52se6QhQ8gE'
    jwt = api.jwt.createJWT(app)

    swagger = Swagger(app, template=template)

    return app
