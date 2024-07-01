
'''
    Business Logic Package
'''

# For db.
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model

# Exports.
from logic.model import logicexceptions

db = SQLAlchemy()
