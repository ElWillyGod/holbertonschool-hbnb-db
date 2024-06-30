
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

    def __init__(self,
            host_id: str,
            name: str,
            description: str,
            number_of_rooms: int,
            number_of_bathrooms: int,
            max_guests: int,
            price_per_night: float,
            latitude: float,
            longitude: float,
            city_id: str,
            amenity_ids: list[str],
            *,
            id: str = None,
            created_at: str = None,
            updated_at: str = None
) -> None:
        super().__init__(id, created_at, updated_at)
        self.host_id = host_id
        self.name = name
        self.description = description
        self.number_of_rooms = number_of_rooms
        self.number_of_bathrooms = number_of_bathrooms
        self.max_guests = max_guests
        self.price_per_night = price_per_night
        self.latitude = latitude
        self.longitude = longitude
        self.city_id = city_id
        self.amenity_ids = amenity_ids
