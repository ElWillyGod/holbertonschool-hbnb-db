
'''
    Defines TrackedObject class.
    This abstract class defines common elements and passes them down to most
    other classes.
'''

from datetime import datetime
from uuid import uuid4
import inspect


class TrackedObjectl:
    '''
        id (str): UUID4 as hex.
        created_at: datetime as string at time of creation.
        updated_at: datetime as string at time of last update.
        update_time() -> None: Updates the updated_at attribute.
        toJson() -> str: Returns a JSON representation of this object.
    '''

    def __init__(self,
                 id: str = None,
                 created_at: str = None,
                 updated_at: str = None):
        now = str(datetime.now())
        self.created_at = now if created_at is None else created_at
        self.updated_at = now if updated_at is None else updated_at
        self.id = uuid4().hex if id is None else id

    def getAllInstanceAttributes(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    def toJson(self) -> str:
        return self.getAllInstanceAttributes()
