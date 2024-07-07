

'''
    Defines the city class.
    A city contains places and is inside a country.
    The name must also be unique in the same country.
'''

from logic.model.trackedobject import TrackedObject
from logic import db

class City(TrackedObject, db.Model):
    '''Cities table'''

    __tablename__ = 'cities'

    name = db.Column(
        db.String(128),
        nullable=False
    )
    country_code = db.Column(
        db.String(2),
        nullable=False
    )

    def __init__(
            self,
            name: str = None,
            country_code: str = None,
            *,
            id: str = None,
            created_at: str = None,
            updated_at: str = None
    ) -> None:
        super().__init__(id, created_at, updated_at)
        """
        if not doesCountryExist(country_code):
            raise CountryNotFoundError(
                f"country '{country_code}' not found")
        if isCityNameDuplicated(name, country_code):
            raise CityNameDuplicated(
                f"{name} already exists in {country_code}")
        """
        self.name = name
        self.country_code = country_code
