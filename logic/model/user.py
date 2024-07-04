'''
    Defines the User class.
    This class is identified by either it's id or it's email,
    as both are unique within the database.
'''

from logic.model.trackedobject import TrackedObject as TObj
from datetime import datetime
from uuid import uuid4
from logic import db
from sqlalchemy import Boolean, Column, String

class User(db.Model):
    """tabla del user"""

    __tablename__ = 'user'

    password = db.Column(db.String(255),
                      nullable=False,
                      primary_key=True)

    firstName = db.Column(db.String(255))

    lastName = db.Column(db.String(255))

    role = db.Column(db.String(255))


"""
class User(db.Model):
    '''
        User Table.
    '''

    __tablename__ = "user"
    __ins = TObj()
    id = __ins.id
    created_at = __ins.created_at
    updated_at = __ins.updated_at

    email = Column(String, unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)

    def toJson(self):
        return {column.name: getattr(self, column.name)
                for column in self.__table__.columns}
"""
