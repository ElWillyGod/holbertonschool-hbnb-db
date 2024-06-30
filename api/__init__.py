
'''
    Package where endpoints and type validations are made.
'''

from flask import Flask
from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.ext.declarative import declarative_base
from api.swagger import template

app = Flask("AirBnB-MWA")
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+mysqldb://root:@localhost/hbnb'
app.config['USE_DATABASE'] = True
db = SQLAlchemy(app)

swagger = Swagger(app, template=template)

import api.amenities
import api.cities
import api.countries
import api.places
import api.reviews
import api.users
