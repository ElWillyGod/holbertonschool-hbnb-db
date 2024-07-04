

'''
    Defines the city class.
    A city contains places and is inside a country.
    The name must also be unique in the same country.
'''

from sqlalchemy import Column, String
from logic.model.trackedobject import TrackedObject
from logic import db

class City(TrackedObject, db.Model):

    __tablename__ = 'city'


    name = db.Column(db.String(255),
                    nullable=False,
                    primary_key=True)

    country_code = db.Column(
        db.String(255),
        nullable=False,
        primary_key=True
    )


    def __init__(self,
                 name: str,
                 country_code: str,
                 *,
                 id: str = None,
                 created_at: str = None,
                 updated_at: str = None,
                 update: dict | None = None
                 ) -> None:
        super().__init__(id, created_at, updated_at)
        """
        if not doesCountryExist(country_code):
            raise CountryNotFoundError(
                f"country '{country_code}' not found")
        if update is None or "name" in update:
            if isCityNameDuplicated(name, country_code):
                raise CityNameDuplicated(
                    f"{name} already exists in {country_code}")
        """
        self.name = name
        self.country_code = country_code

"""
class City(db.Model):

    __tablename__ = 'city'
    __ins = TObj()
    id = __ins.id
    created_at = __ins.created_at
    updated_at = __ins.updated_at

    name = Column(String(255), nullable=False)
    countryCode = Column(String(3), nullable=False)

    def toJson(self):
        return {column.name: getattr(self, column.name)
                for column in self.__table__.columns}
"""
