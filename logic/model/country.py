
'''
    Defines the Country class.
    A country has cities.
    Instead of an ID they have a code.
    They also lack creation datetime and update datetime.
'''

from model import Base

from sqlalchemy import Column, String


class Country(Base):
    """
        Country table.
    """

    __tablename__ = 'country'
    code = Column(String(3), unique=True)
    name = Column(String(255), unique=True)
