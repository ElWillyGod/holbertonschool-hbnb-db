

'''
    Defines the city class.
    A city contains places and is inside a country.
    The name must also be unique in the same country.
'''

from logic.model.trackedobject import TrackedObject

from sqlalchemy import Column, String


class City(TrackedObject):

    __tablename__ = 'city'
    name = Column(String(255), nullable=False)
    countryCode = Column(String(3), nullable=False)

    def __init__(
            self,
            name: str,
            country_code: str,
            *,
            id: str = None,
            created_at: str = None,
            updated_at: str = None
) -> None:
        super().__init__(id, created_at, updated_at)
        self.name = name
        self.country_code = country_code
