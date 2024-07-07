'''
    Defines the User class.
    This class is identified by either it's id or it's email,
    as both are unique within the database.
'''

from logic.model.trackedobject import TrackedObject as TObj
from logic import db

class User(TObj, db.Model):
    '''Users table'''

    __tablename__ = 'users'

    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)

    def __init__(
            self,
            email: str = None,
            password: str = None,
            first_name: str = None,
            last_name: str = None,
            is_admin: str = None,
            *,
            id = None,
            created_at = None,
            updated_at = None
        ) -> None:
        super().__init__(id, created_at, updated_at)
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.is_admin = is_admin
