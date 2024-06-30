
'''
    Package where endpoints, authorizations and type validations are made.

    TODO:
    - I have no idea how to implement token auth into swagger, I only placed
    the correct codes to expect.
    - Test auth.
'''

import json
from os import environ
from pathlib import Path
from flask import Flask

from flask_cors import CORS

import api.security as security

from api.blueprints import *

import api.home_redirection as home_redirection

from flasgger import Swagger

from persistence import db


def appFactory() -> Flask:
    '''
        Creates an app using:

            Configurations from config.py. Also .env and .flaskenv from root
            affect some configs.

            CORS (Cross-Origin Resource Sharing) to fix swagger on gunicorn.

            JWT, for authorization, bcrypt for hashing. Also registers login
            endpoint.

            Registers all blueprints from blueprints package (fancy endpoints).

            Also registers home page ("/") to a redirect to apidocs.

            Swagger, for documentation.
    '''

    # Creates app and adds configs.
    app = Flask(__name__)
    app.config.from_pyfile("settings.py")
    app.url_map.strict_slashes = False

    # Enables Cross-Origin Resource Sharing on all paths.
    # Placed to fix swagger issues when running gunicorn.
    # I sincerely have no idea what it does but it works.
    CORS(app)

    # Initializes jwc and bcrypt. Also registers login endpoint.
    security.associateSecurity(app)
    app.register_blueprint(security.login_bp)

    # Initializes sqlalchemy on flask.
    db.init_app(app)

    # Registers all endpoint blueprints.
    app.register_blueprint(amenities.bp)
    app.register_blueprint(countries.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(cities.bp)
    app.register_blueprint(places.bp)
    app.register_blueprint(reviews.bp)

    # Redirects homepage ("/") to apidocs
    app.register_blueprint(home_redirection.bp)

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

    # Returns app to be runned as flask or gunicorn, in root.
    return app
