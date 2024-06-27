
'''
    Defines the User class.
    This class is identified by either it's id or it's email,
    as both are unique within the database.
'''

from logic.model.trackedobject import TrackedObject
from logic.model.validationlib import isUserEmailDuplicated
from logic.model.logicexceptions import EmailDuplicated
from logic import bcrypt


class User(TrackedObject):
    '''
        User Class.
    '''

    def __init__(self,
                 email: str,
                 first_name: str,
                 last_name: str,
                 password: str,
                 is_admin: bool = False,
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
        self.is_admin = is_admin
        self.password = bcrypt.generate_password_hash(password, 16)
