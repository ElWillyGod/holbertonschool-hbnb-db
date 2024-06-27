
'''
    Defines how to authorize endpoints using JWT and bcrypt.
    Also defines login endpoint.
'''

from flask_jwt_extended import JWTManager, create_access_token
from flask import request, Blueprint
import flask_bcrypt
from logic.logicfacade import LogicFacade
from logic import logicexceptions


jwt = JWTManager()
bcrypt = flask_bcrypt.Bcrypt()
login_bp = Blueprint("login", __name__)


# Called from init
def associateSecurity(app):
    jwt.init_app(app)
    bcrypt.init_app(app)


@login_bp.post('/login')
def login():
    """
        Here goes swag.
    """

    WRONG_DATA = "Wrong email or password"

    # Get user request info
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    # Fetch user data by email. 401 if email not found.
    try:
        hashed_password = LogicFacade.getPasswordByEmail(email)
    except logicexceptions.IDNotFoundError:
        return WRONG_DATA, 401

    # Compare passwords. 401 if different.
    if bcrypt.check_password_hash(hashed_password, password):
        access_token = create_access_token(identity=email)
        return {"access_token": access_token}, 200
    return WRONG_DATA, 401
