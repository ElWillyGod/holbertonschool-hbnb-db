from sqlalchemy import Column, Integer, String, TIMESTAMP, create_engine
from api import db


def createAmenity(id, data):

    ameni = Amenity(id='{}'.format(id), name=data.get('name'), created_at='1999-12-31 23:59:59', update_at='1999-12-31 23:59:59')

