
'''
    Defines the Place Class.
'''
from logic.model.trackedobject import TrackedObject
from logic.model.amenity import Amenity
from logic import db
from persistence import dm

place_amenities = db.Table('place_amenities', db.metadata,
    db.Column('place_id', db.String(32), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(32), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(TrackedObject, db.Model):
    '''Places table'''

    __tablename__ = 'places'

    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(1024), nullable=False)
    number_of_rooms = db.Column(db.Integer, nullable=False)
    number_of_bathrooms = db.Column(db.Integer, nullable=False)
    max_guests = db.Column(db.Integer, nullable=False)
    price_per_night = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    host_id = db.Column(
        db.String(32),
        db.ForeignKey('users.id'),
        nullable=False,
    )
    city_id = db.Column(
        db.String(32),
        db.ForeignKey('cities.id'),
        nullable=False
    )
    amenity_ids = db.relationship(
        'Amenity',
        secondary=place_amenities,
        lazy='subquery'
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
        self.amenity_ids = []
        if amenity_ids is not None:
            for amenity_id in amenity_ids:
                self.amenity_ids.append(dm.read(Amenity(id=amenity_id)))

    # Importante
    def getAllInstanceAttributes(self):
            columns = {column.name: getattr(self, column.name) for column in self.__table__.columns}
            if self.amenity_ids is not None:
                columns["amenity_ids"] = [amenity.id for amenity in self.amenity_ids]
            return columns
