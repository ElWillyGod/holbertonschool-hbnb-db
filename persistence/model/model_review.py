from sqlalchemy.orm import Session
import base
from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, create_engine, engine


class review(base.Base):

    __tablename__ = 'review'

    id = Column(Integer,
                nullable=False,
                primary_key=True)

    placeId = Column(Integer,
                     ForeignKey('place.id'),
                     nullable=False,
                     primary_key=True)

    userId = Column(Integer,
                    ForeignKey('user.id'),
                    nullable=False,
                    primary_key=True)

    reating = Column(Integer,
                     nullable=False)

    create_at = Column(TIMESTAMP,
                       nullable=False)

    update_at = Column(TIMESTAMP,
                       nullable=False)

