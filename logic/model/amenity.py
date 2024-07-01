
'''
    Defines the amenity class.
    An amenity is something that places have.
'''

from logic.model.trackedobject import TrackedObject as TObj
from sqlalchemy import Column, String
from logic import db


class Amenity(db.Model):
    '''
        Amenity Class.
    '''

    __tablename__ = 'amenity'
    __ins = TObj()
    id = __ins.id
    created_at = __ins.created_at
    updated_at = __ins.updated_at

    names = Column(String(255), unique=True)

    def toJson(self):
        return {column.name: getattr(self, column.name)
                for column in self.__table__.columns}
