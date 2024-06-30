
'''
    Defines the Place Class.
'''

from logic.model.trackedobject import TrackedObject
from logic.model.validationlib import idExists
from logic.model.logicexceptions import IDNotFoundError

from sqlalchemy import Column, Float, ForeignKey, Integer, String, TIMESTAMP
from persistence import db


class Place(TrackedObject, db.Model):

    __tablename__ = 'place'

    id = db.Column(db.Integer,
                nullable=False,
                primary_key=True)

    userId = db.Column(db.Integer,
                    ForeignKey('user.id'),
                    nullable=False,
                    primary_key=True)

    name = db.Column(db.String(255),
                  nullable=False)

    description = db.Column(db.String(255),
                         nullable=False)

    numberOfRooms = db.Column(db.Integer,
                           nullable=False)

    numberOfBathrooms = db.Column(db.Integer,
                               nullable=False)

    maxGues = db.Column(db.Integer,
                     nullable=False)

    pricePreNigth = db.Column(db.Float,
                           nullable=False)

    latitude = db.Column(db.Float,
                      nullable=False)

    longitude = db.Column(db.Float,
                       nullable=False)

    citiId = db.Column(db.Integer,
                    ForeignKey('city.id'),
                    nullable=False)

    create_at = db.Column(db.TIMESTAMP,
                       nullable=False)

    update_at = db.Column(db.TIMESTAMP,
                       nullable=False)

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
                 updated_at: str = None,
                 update: dict | None = None
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
