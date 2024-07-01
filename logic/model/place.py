
'''
    Defines the Place Class.
'''

from sqlalchemy import Column, Float, ForeignKey, Integer, String
from logic.model.trackedobject import TrackedObject as TObj
from logic.model.city import City
from logic.model.user import User
from logic import db


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
