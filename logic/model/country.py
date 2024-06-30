
'''
    Defines the Country class.
    A country has cities.
    Instead of an ID they have a code.
    They also lack creation datetime and update datetime.
'''

from logic import Base

from sqlalchemy import Column, String


class Country(Base):
    """
        Country table.
    """

    __tablename__ = 'country'
    code = Column(String(3), primary_key=True)
    name = Column(String(255), unique=True)
