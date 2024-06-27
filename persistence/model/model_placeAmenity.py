from sqlalchemy import Column, ForeignKey, Integer
import base


class placeAmenity(base.Base):

    __tablename__ = 'placeAmenity'

    idPlace = Column(Integer,
                     ForeignKey('place.id'))

    idAmenities = Column(Integer,
                         ForeignKey('amenity.id'))
