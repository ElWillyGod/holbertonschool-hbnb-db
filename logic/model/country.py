
'''
    Defines the Country class.
    A country has cities.
    Instead of an ID they have a code.
    They also lack creation datetime and update datetime.
'''

from logic import db
from sqlalchemy import Column, String


class Country(db.Model):
    """
        Country table.
    """

    __tablename__ = 'country'
    code = Column(String(3), primary_key=True, unique=True)
    name = Column(String(255), unique=True)

    def toJson(self):
        return {column.name: getattr(self, column.name)
                for column in self.__table__.columns}
