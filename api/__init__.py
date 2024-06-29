
'''
    Package where endpoints, authorizations and type validations are made.
'''

from flask import Flask

import api.security as security

from api.blueprints import *

from flasgger import Swagger


def appFactory() -> Flask:
    '''
        Creates an app using:

            All blueprints from blueprints (endpoints).

            JWT, for authorization, bcrypt for hashing.

            Swagger, for documentation.
    '''

    app = Flask(__name__)
    app.config.from_pyfile("settings.py")
    app.url_map.strict_slashes = False

    security.associateSecurity(app)
    app.register_blueprint(security.login_bp)

    app.register_blueprint(amenities.bp)
    app.register_blueprint(countries.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(cities.bp)
    app.register_blueprint(places.bp)
    app.register_blueprint(reviews.bp)

    Swagger(app, template_file="blueprints/swagger/swagger.yaml")

    return app
