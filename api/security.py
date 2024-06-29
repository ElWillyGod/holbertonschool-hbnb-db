
'''
    Defines how to authorize endpoints using JWT and bcrypt.
    Also defines login endpoint.
'''

from flask_jwt_extended import JWTManager, create_access_token
from flask import request, Blueprint, jsonify, Response
import flask_bcrypt
from logic.logicfacade import LogicFacade

jwt = JWTManager()
bcrypt = flask_bcrypt.Bcrypt()
login_bp = Blueprint("login", __name__)


# Called from init.
def associateSecurity(app):
    jwt.init_app(app)
    bcrypt.init_app(app)


# Called in users.
def hashPassword(password):
    return bcrypt.generate_password_hash(password, 16)


@jwt.unauthorized_loader
def handle_unauthorized_error(err):
    return {"error": "401 Unauthorized"}, 401


@jwt.invalid_token_loader
def handle_invalid_token_error(err):
    return {"error": "401 Unauthorized"}, 401


@jwt.expired_token_loader
def handle_expired_token_error(err):
    return {"error": "401 Unauthorized"}, 401


@jwt.revoked_token_loader
def handle_revoked_token_error(err):
    return {"error": "401 Unauthorized"}, 401


@jwt.needs_fresh_token_loader
def handle_needs_fresh_token_error(err):
    return {"error": "401 Unauthorized"}, 401


@login_bp.post('/login')
def login():
    """
        Here be swag.
    """

    WRONG_FIELDS = "Wrong email or password"
    WRONG_DATA = "Wrong email or password"

    # Get user request info
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    # Checks if request info is ok. 400 if not.
    if email is None or password is None:
        return WRONG_FIELDS, 400

    # Fetch user data by email. 401 if email not found.
    hashed_password, is_admin = LogicFacade.getPswdAndAdminByEmail(email)
    if hashed_password is None:
        return WRONG_DATA, 401

    # Compare passwords. 401 if different.
    if bcrypt.check_password_hash(hashed_password, password):
        # Create token.
        access_token = create_access_token(
            identity=email,
            additional_claims={"is_admin": True}
            )
        return {"access_token": access_token}, 200
    else:
        return WRONG_DATA, 401
