

'''
    Defines the city class.
    A city contains places and is inside a country.
    The name must also be unique in the same country.
'''

from logic.model.trackedobject import TrackedObject

from sqlalchemy import Column, String


class City(TrackedObject):

    __tablename__ = 'city'
    name = Column(String(255), nullable=False)
    countryCode = Column(String(3), nullable=False)
