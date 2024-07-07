
'''
    Defines the amenity class.
    An amenity is something that places have.
'''

from logic.model.trackedobject import TrackedObject
from logic import db

class Amenity(TrackedObject, db.Model):
    '''Amenities table'''

    __tablename__ = 'amenities'

    name = db.Column(
        db.String(64),
        unique=True,
        nullable=False
    )

    def __init__(
            self,
            name: str = None,
            *,
            id: str = None,
            created_at: str = None,
            updated_at: str = None
    ) -> None:
        super().__init__(id, created_at, updated_at)
        """
        if isAmenityDuplicated(name):
            raise AmenityNameDuplicated("amenity already exists")
        """
        self.name = name
