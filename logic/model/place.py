
'''
    Defines the Place Class.
'''

from sqlalchemy import Column, Float, ForeignKey, Integer, String
from logic.model.trackedobject import TrackedObject
from logic.model.city import City
from logic.model.user import User
from logic import db

class Place(TrackedObject, db.Model):

    __tablename__ = 'place'


    user_id = db.Column(db.Integer,
                    ForeignKey('user.id'),
                    nullable=False,
                    primary_key=True)

    name = db.Column(db.String(255), nullable=False)

    description = db.Column(db.String(255), nullable=False)

    number_of_rooms = db.Column(db.Integer, nullable=False)

    number_of_bathrooms = db.Column(db.Integer, nullable=False)

    max_guests = db.Column(db.Integer, nullable=False)

    price_per_night = db.Column(db.Float, nullable=False)

    latitude = db.Column(db.Float, nullable=False)

    longitude = db.Column(db.Float, nullable=False)

    city_id = db.Column(
        db.Integer,
        ForeignKey('city.id'),
        nullable=False
    )

    def __init__(
            self,
            host_id: str = None,
            name: str = None,
            description: str = None,
            number_of_rooms: int = None,
            number_of_bathrooms: int = None,
            max_guests: int = None,
            price_per_night: float = None,
            latitude: float = None,
            longitude: float = None,
            city_id: str = None,
            amenity_ids: list[str] = None,
            *,
            id: str = None,
            created_at: str = None,
            updated_at: str = None
    ) -> None:
        super().__init__(id, created_at, updated_at)
        """
        if not idExists(host_id, "users"):
            raise IDNotFoundError("host_id does not exist")
        if not idExists(city_id, "cities"):
            raise IDNotFoundError("city_id does not exist")
        for id in amenity_ids:
            if not idExists(id, "amenities"):
                raise IDNotFoundError(f"'{id}' in amenity_ids does not exist")
                """
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

"""
class Place(db.Model):
    '''
        Place table.
    '''

    __tablename__ = 'place'
    __ins = TObj()
    id = __ins.id
    created_at = __ins.created_at
    updated_at = __ins.updated_at

    host_id = Column(Integer, ForeignKey(User.id), nullable=False)
    cname = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    number_of_rooms = Column(Integer, nullable=False)
    number_of_bathrooms = Column(Integer,  nullable=False)
    max_guests = Column(Integer, nullable=False)
    price_per_night = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    city_id = Column(Integer, ForeignKey(City.id), nullable=False)

    def toJson(self):
        return {column.name: getattr(self, column.name)
                for column in self.__table__.columns}

"""
