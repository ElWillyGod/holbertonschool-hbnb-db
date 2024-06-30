
'''
    Defines the amenity class.
    An amenity is something that places have.
'''

from logic.model.trackedobject import TrackedObject
from sqlalchemy import Column, String


class Amenity(TrackedObject):
    '''
        Amenity Class.
    '''

    __tablename__ = 'amenity'
    name = Column(String(255), unique=True)

    def __init__(
            self,
            name: str,
            *,
            id: str = None,
            created_at: str = None,
            updated_at: str = None
) -> None:
        super().__init__(id, created_at, updated_at)
        self.name = name
