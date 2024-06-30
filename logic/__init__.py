
'''
    Business Logic Package
'''

# For db.
from flask_sqlalchemy import SQLAlchemy

# Exports.
from logic.model import logicexceptions

db = SQLAlchemy()
Base = db.Model
