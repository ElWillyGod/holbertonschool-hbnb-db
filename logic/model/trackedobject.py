
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
         db.String(32),
         nullable=False,
         primary_key=True
    )

    created_at = db.Column(
         db.DateTime(timezone=True),
         default=str(db.func.current_timestamp())
    )
    updated_at = db.Column(
         db.DateTime(timezone=True),
         onupdate=str(db.func.current_timestamp())
    )

    def __init__(
            self,
            id: str = None,
            created_at = None,
            updated_at = None
    ):
        self.created_at = created_at
        self.updated_at = updated_at
        self.id = str(uuid4().hex) if id is None else id

    def getAllInstanceAttributes(self):
            return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    def toJson(self) -> str:
        return self.getAllInstanceAttributes()
