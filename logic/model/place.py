
'''
    Defines the Place Class.
'''

from logic.model.trackedobject import TrackedObject
from logic.model.city import city
from logic.model.user import user

from sqlalchemy import Column, Float, ForeignKey, Integer, String


class Place(TrackedObject):
    '''
        Place table.
    '''

    __tablename__ = 'place'
    host_id = Column(Integer, ForeignKey(user.id), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    number_of_rooms = Column(Integer, nullable=False)
    number_of_bathrooms = Column(Integer,  nullable=False)
    max_guests = Column(Integer, nullable=False)
    price_per_night = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    city_id = Column(Integer, ForeignKey(city.id), nullable=False)

    def __init__(self, **kwargs):
        super.__init__(**kwargs)
        self.amenity_ids = kwargs.get("amenity_ids")
