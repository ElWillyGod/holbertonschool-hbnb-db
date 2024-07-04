
'''
    Defines TrackedObject class.
    This abstract class defines common elements and passes them down to most
    other classes.
'''

from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String
from logic import db

class TrackedObject:
    '''
        id (str): UUID4 as hex.
        created_at: datetime as string at time of creation.
        updated_at: datetime as string at time of last update.
        update_time() -> None: Updates the updated_at attribute.
        toJson() -> str: Returns a JSON representation of this object.
    '''
    id = db.Column(
         db.String(255),
         nullable=False,
         primary_key=True
    )

    created_at = db.Column(
         db.String(255),
         default=str(db.func.current_timestamp())
    )
    updated_at = db.Column(
         db.String(255),
         onupdate=str(db.func.current_timestamp())
    )

    def __init__(self,
                 id: str = None,
                 created_at: str = None,
                 updated_at: str = None
    ):
        now = str(datetime.now())
        self.created_at = now if created_at is None else created_at
        self.updated_at = now if updated_at is None else updated_at
        self.id = str(uuid4().hex) if id is None else id

    def getAllInstanceAttributes(self):
            return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    def toJson(self) -> str:
        return self.getAllInstanceAttributes()

"""
class TrackedObject():
    '''
        Tracked object column creator.
    '''

    def __init__(self) -> None:
        self.id = Column(String(255), default=uuid4().hex,
                    nullable=False, primary_key=True, unique=True)
        self.created_at = Column(String, default=str(datetime.now()), nullable=False)
        self.updated_at = Column(String, default=str(datetime.now()), nullable=False)
"""
