
'''
    Defines the Country class.
    A country has cities.
    Instead of an ID they have a code.
    They also lack creation datetime and update datetime.
'''

from logic.model.validationlib import doesCountryExist
from logic.model.logicexceptions import CountryNotFoundError
from model import Base

from sqlalchemy import Column, String


class Country(Base):
    """
        Country table.
    """

    __tablename__ = 'country'
    code = Column(String(3), unique=True)
    name = Column(String(255), unique=True)

    def __init__(
            self,
            code: str,
            name: str
) -> None:
        if not doesCountryExist(code):
            raise CountryNotFoundError("country does not exist")
        self.code = code
        self.name = name
