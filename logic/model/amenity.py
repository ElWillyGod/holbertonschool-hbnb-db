
'''
    Defines the amenity class.
    An amenity is something that places have.
'''

from enum import unique
from logic.model.trackedobject import TrackedObject
from sqlalchemy import Column, String
from logic import db

class Amenity(TrackedObject, db.Model):
    '''
        Amenity Class.
    '''

    __tablename__ = 'amenity'
    name = db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )


    """

    created_at = db.Column(db.String(255),
                               nullable=False)

    updated_at = db.Column(db.String(255),
                              nullable=False)
    """

    def __init__(self,
                 name: str = None,
                 *,
                 id: str = None,
                 created_at: str = None,
                 updated_at: str = None
                 ) -> None:
        super().__init__(id, created_at, updated_at)
        """
        if update is None or "name" in update:
            if isAmenityDuplicated(name):
                raise AmenityNameDuplicated("amenity already exists")
                """
        self.name = name

"""
class Amenity(db.Model):
    '''
        Amenity Class.
    '''

    __tablename__ = 'amenity'
    __ins = TObj()
    id = __ins.id
    created_at = __ins.created_at
    updated_at = __ins.updated_at

    name = Column(String(255), unique=True)

    def toJson(self):
        return {column.name: getattr(self, column.name)
                for column in self.__table__.columns}

"""
