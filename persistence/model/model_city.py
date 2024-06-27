from sqlalchemy import Column, Integer, String, TIMESTAMP
import base


class city(base.Base):

    __tablename__ = 'city'

    id = Column(Integer,
                nullable=False,
                primary_key=True)

    name = Column(String(255),
                  nullable=False,
                  primary_key=True)

    countryCode = Column(String(255),
                         nullable=False,
                         primary_key=True)

    create_at = Column(TIMESTAMP,
                       nullable=False)

    update_at = Column(TIMESTAMP,
                       nullable=False)
