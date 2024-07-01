

'''
    Defines the city class.
    A city contains places and is inside a country.
    The name must also be unique in the same country.
'''

from sqlalchemy import Column, String
from logic.model.trackedobject import TrackedObject as TObj
from logic import db


class City(db.Model):

    __tablename__ = 'city'
    __ins = TObj()
    id = __ins.id
    created_at = __ins.created_at
    updated_at = __ins.updated_at

    name = Column(String(255), nullable=False)
    countryCode = Column(String(3), nullable=False)

    def toJson(self):
        return {column.name: getattr(self, column.name)
                for column in self.__table__.columns}
