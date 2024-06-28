from sqlalchemy import Column, Integer, String, TIMESTAMP, create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy

Base = declarative_base()


class Amenity(Base):

    __tablename__ = 'amenity'

    id = Column(String,
                nullable=False,
                primary_key=True)

    name = Column(String(255),
                  primary_key=True)

    created_at = Column(TIMESTAMP,
                       nullable=False)

    update_at = Column(TIMESTAMP,
                       nullable=False)


def createAmenity(id, data):

    engine = create_engine('mysql+mysqldb://root:@localhost/hbnb'
                           , pool_pre_ping=True)


    session = Session(engine)

    ameni = Amenity(id='{}'.format(id), name=data.get('name'), created_at='1999-12-31 23:59:59', update_at='1999-12-31 23:59:59')

    session.add(ameni)
    session.commit()

    print(ameni.name)

    session.close()

    result = {
            'entity': data,
            'entity_type': 'users'
        }

    return result