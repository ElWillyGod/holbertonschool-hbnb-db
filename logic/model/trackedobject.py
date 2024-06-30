
'''
    Defines TrackedObject class.
    This abstract class defines common elements and passes them down to most
    other classes.
'''

from datetime import datetime
from uuid import uuid4
from model import Base
from sqlalchemy import Column, Integer, TIMESTAMP

class TrackedObject(Base):
    '''
        Tracked table.
    '''

    id = Column(Integer, nullable=False, primary_key=True)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)

    def __init__(
            self,
            id: str = None,
            created_at: str = None,
            updated_at: str = None
) -> None:
        now = str(datetime.now())
        self.created_at = now if created_at is None else created_at
        self.updated_at = now if updated_at is None else updated_at
        self.id = uuid4().hex if id is None else id

    def getAllInstanceAttributes(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    def toJson(self) -> str:
        return self.getAllInstanceAttributes()
