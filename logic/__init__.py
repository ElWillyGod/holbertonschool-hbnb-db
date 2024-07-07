
'''
    Business Logic Package
'''

# For db.
from flask_sqlalchemy.model import Model
from logic.sqlalchemy_class import MySQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Exports.
from logic.model import logicexceptions

db = SQLAlchemy()
