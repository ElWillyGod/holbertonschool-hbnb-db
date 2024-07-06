'''
    Defines the User class.
    This class is identified by either it's id or it's email,
    as both are unique within the database.
'''

from logic.model.trackedobject import TrackedObject as TObj
from logic import db

class User(TObj, db.Model):
    """tabla del user"""

    __tablename__ = 'user'

    email = db.Column(db.String(255), nullable=False, unique=True)

    password = db.Column(db.String(255), nullable=False)

    first_name = db.Column(db.String(255), nullable=False)

    last_name = db.Column(db.String(255), nullable=False)

    is_admin = db.Column(db.Boolean, nullable=False)

    def __init__(
            self,
            email: str = None,
            password: str = None,
            first_name: str = None,
            last_name: str = None,
            is_admin: str = None,
            id: str = None,
            created_at: str = None,
            updated_at: str = None
        ) -> None:
        super().__init__(id, created_at, updated_at)
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.is_admin = is_admin

"""
class User(db.Model):
    '''
        User Table.
    '''

    __tablename__ = "user"
    __ins = TObj()
    id = __ins.id
    created_at = __ins.created_at
    updated_at = __ins.updated_at

    email = Column(String, unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)

    def toJson(self):
        return {column.name: getattr(self, column.name)
                for column in self.__table__.columns}
"""
