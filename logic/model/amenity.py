
'''
    Defines the amenity class.
    An amenity is something that places have.
'''

from logic.model.trackedobject import TrackedObject
from logic.model.validationlib import isAmenityDuplicated
from logic.model.logicexceptions import AmenityNameDuplicated
from api import db
from sqlalchemy import column, String, TIMESTAMP


class Amenity(TrackedObject, db.Model):
    '''
        Amenity Class.
    '''

    __tablename__ = 'amenity'
    name = db.Column(db.String(255),
                         primary_key=True)

    id = db.Column(db.String,
                       nullable=False,
                       primary_key=True)

    created_at = db.Column(db.TIMESTAMP,
                               nullable=False)

    update_at = db.Column(db.TIMESTAMP,
                              nullable=False)

    def __init__(self,
                 name: str,
                 *,
                 id: str = None,
                 created_at: str = None,
                 updated_at: str = None,
                 update: dict | None = None
                 ) -> None:
        super().__init__(id, created_at, updated_at)
        """
        if update is None or "name" in update:
            if isAmenityDuplicated(name):
                raise AmenityNameDuplicated("amenity already exists")
                """
        self.name = name
