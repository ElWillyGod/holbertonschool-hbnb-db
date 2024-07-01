
'''
    Defines TrackedObject class.
    This abstract class defines common elements and passes them down to most
    other classes.
'''

from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String

class TrackedObject():
    '''
        Tracked object column creator.
    '''

    def __init__(self) -> None:
        self.id = Column(String(255), default=uuid4().hex,
                    nullable=False, primary_key=True, unique=True)
        self.created_at = Column(String, default=str(datetime.now()), nullable=False)
        self.updated_at = Column(String, default=str(datetime.now()), nullable=False)
