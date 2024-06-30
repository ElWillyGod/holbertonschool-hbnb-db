import base
from sqlalchemy import Column, Integer, String, TIMESTAMP


class User(base.Base):
    """tabla del user"""

    __tablename__ = 'user'

    id = Column(Integer,
                nullable=False,
                primary_key=True)

    password = Column(String(255),
                      nullable=False,
                      primary_key=True)

    firstName = Column(String(255))

    lastName = Column(String(255))

    role = Column(String(255))

    create_at = Column(TIMESTAMP,
                       nullable=False)

    update_at = Column(TIMESTAMP,
                       nullable=False)
