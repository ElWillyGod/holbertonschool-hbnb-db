
'''
    Defines the amenity class.
    An amenity is something that places have.
'''

from logic.model.trackedobject import TrackedObject
from sqlalchemy import Column, String


class Amenity(TrackedObject):
    '''
        Amenity Class.
    '''

    __tablename__ = 'amenity'
    names = Column(String(255), unique=True)
