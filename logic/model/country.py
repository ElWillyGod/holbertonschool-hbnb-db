
'''
    Defines the Country class.
    A country has cities.
    Instead of an ID they have a code.
    They also lack creation datetime and update datetime.
'''

from logic import db


class Country(db.Model):
    '''Countries table'''

    __tablename__ = 'countries'

    code = db.Column(db.String(2), primary_key=True, unique=True)
    name = db.Column(db.String(128), unique=True)

    def __init__(
            self,
            code: str = None,
            name: str = None
    ) -> None:
        self.code = code
        self.name = name

    def toJson(self):
        return {column.name: getattr(self, column.name)
                for column in self.__table__.columns}
