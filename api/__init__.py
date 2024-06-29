
'''
    Package where endpoints, authorizations and type validations are made.
'''

import json
from os import environ
from pathlib import Path
from flask import Flask

from flask_cors import CORS

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

    # Creates app.
    app = Flask(__name__)
    app.config.from_pyfile("settings.py")
    app.url_map.strict_slashes = False

    # Enables Cross-Origin Resource Sharing on all paths.
    # Placed to fix swagger issues when running gunicorn.
    CORS(app)

    # Initialized jwc and bcrypt.
    security.associateSecurity(app)
    app.register_blueprint(security.login_bp)

    # Registers all endpoint blueprints.
    app.register_blueprint(amenities.bp)
    app.register_blueprint(countries.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(cities.bp)
    app.register_blueprint(places.bp)
    app.register_blueprint(reviews.bp)

    # Assigns template to Swagger.
    # If runned with gunicorn, it overwrites the host attr to gunicorn's
    # assigned domain and port.
    template = {}
    parent_path = Path(__file__).parent.resolve()
    with open(f"{parent_path}/blueprints/swagger/swagger.json", "r") as f:
        template: dict = json.load(f)
    if host := environ.get("RUNNING_GUNICORN"):
        template["host"] = host
    Swagger(app, template=template)

    # Returns app to be runned as flask or gunicorn in root.
    return app
