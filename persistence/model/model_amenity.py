from sqlalchemy import Column, Integer, String, TIMESTAMP
import base


class amenity(base.Base):

    __tablename__ = 'amenity'

    id = Column(Integer,
                nullable=False,
                primary_key=True)

    name = Column(String(255),
                  primary_key=True)

    create_at = Column(TIMESTAMP,
                       nullable=False)

    update_at = Column(TIMESTAMP,
                       nullable=False)
