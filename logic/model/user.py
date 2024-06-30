'''
    Defines the User class.
    This class is identified by either it's id or it's email,
    as both are unique within the database.
'''

from logic.model.trackedobject import TrackedObject
from sqlalchemy import Column, String, Boolean


class User(TrackedObject):
    '''
        User Table.
    '''

    __tablename__ = 'user'
    email = Column(String, unique=True)
    password = Column(String(255), nullable=False)
    first_name = Column(String(255))
    last_name = Column(String(255))
    is_admin = Column(Boolean)
