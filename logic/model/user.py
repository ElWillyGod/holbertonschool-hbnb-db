
'''
    Defines the User class.
    This class is identified by either it's id or it's email,
    as both are unique within the database.
'''

from logic.model.trackedobject import TrackedObject
from logic.model.validationlib import isUserEmailDuplicated
from logic.model.logicexceptions import EmailDuplicated
from api import db
from sqlalchemy import Column, Integer, String, TIMESTAMP


class User(db.Model):
    """tabla del user"""

    __tablename__ = 'user'

    id = db.Column(db.Integer,
                nullable=False,
                primary_key=True)

    password = db.Column(db.String(255),
                      nullable=False,
                      primary_key=True)

    firstName = db.Column(db.String(255))

    lastName = db.Column(db.String(255))

    role = db.Column(db.String(255))

    create_at = db.Column(db.TIMESTAMP,
                       nullable=False)

    update_at = db.Column(db.TIMESTAMP,
                       nullable=False)
"""
class User(TrackedObject):
    '''
        User Class.
    '''
 
    def __init__(self,
                 email: str,
                 first_name: str,
                 last_name: str,
                 *,
                 id: str = None,
                 created_at: str = None,
                 updated_at: str = None,
                 update: dict | None = None
                 ) -> None:

        super().__init__(id, created_at, updated_at)
        if update is None or "email" in update:
            if isUserEmailDuplicated(email):
                raise EmailDuplicated("email already exists")
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

        """
