from sqlalchemy import Column, Float, ForeignKey, Integer, String, TIMESTAMP
import base


class place(base.Base):

    __tablename__ = 'place'

    id = Column(Integer,
                nullable=False,
                primary_key=True)

    userId = Column(Integer,
                    ForeignKey('user.id'),
                    nullslast=False,
                    primary_key=True)

    name = Column(String(255),
                  nullable=False)

    description = Column(String(255),
                         nullable=False)

    numberOfRooms = Column(Integer,
                           nullable=False)

    numberOfBathrooms = Column(Integer,
                               nullable=False)

    maxGues = Column(Integer,
                     nullable=False)

    pricePreNigth = Column(Float,
                           nullable=False)

    latitude = Column(Float,
                      nullable=False)

    longitude = Column(Float,
                       nullable=False)

    citiId = Column(Integer,
                    ForeignKey('city.id'),
                    nullable=False)

    create_at = Column(TIMESTAMP,
                       nullable=False)

    update_at = Column(TIMESTAMP,
                       nullable=False)
