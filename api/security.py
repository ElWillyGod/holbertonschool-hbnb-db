
'''
    Implements authentication and authorization by tokens for using
    JWT and bcrypt modules. More authorization is done in BL.

    Also defines login endpoint.
'''

from flask_jwt_extended import JWTManager, create_access_token
from flask import request, Blueprint
import flask_bcrypt
from logic import logicexceptions
from logic.logicfacade import LogicFacade
from flasgger import swag_from

# Instanciates all required objects.
jwt = JWTManager()
bcrypt = flask_bcrypt.Bcrypt()
login_bp = Blueprint("login", __name__)


# Called from init to attach to app.
def associateSecurity(app):
    jwt.init_app(app)
    bcrypt.init_app(app)


# Called in users endpoint on post and update to hash user password.
def hashPassword(password):
    return bcrypt.generate_password_hash(password, 16).decode('utf-8')


# Authentication error handlers.
@jwt.unauthorized_loader
def handle_unauthorized_error(err):
    return {"error": "Unauthenticated"}, 401


@jwt.invalid_token_loader
def handle_invalid_token_error(err):
    return {"error": "Invalid token"}, 401


@jwt.expired_token_loader
def handle_expired_token_error(err):
    return {"error": "Expired token"}, 401


@jwt.revoked_token_loader
def handle_revoked_token_error(err):
    return {"error": "Revoked token"}, 401


@jwt.needs_fresh_token_loader
def handle_needs_fresh_token_error(err):
    return {"error": "Needs fresh token"}, 401


@login_bp.post('/login')
@swag_from("blueprints/swagger/login.yaml")
def login():
    '''
        Login endpoint for users to authenticate.

        Returns as response a token that must be used to authenticate the
        user identity.
    '''

    WRONG_FIELDS = {"error": "needs email and password"}
    WRONG_DATA = {"error": "wrong email or password"}

    # Get user request info.
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    # Checks if request info is ok. 400 if not.
    if email is None or password is None:
        return WRONG_FIELDS, 400

    # Fetch user data by email. 401 if email not found.
    try:
        hashed_password, user_id, is_admin = (
            LogicFacade.getPswdAndAdminByEmail(email)
            )
    except logicexceptions.EmailNotFoundError as err:
        return WRONG_DATA, 401

    # Compare passwords. 401 if different.
    if bcrypt.check_password_hash(hashed_password, password):
        # Create token.
        access_token = create_access_token(
            identity=email,
            additional_claims={
                "is_admin": is_admin,
                "user_id": user_id
                }
        )

        return {"access_token": access_token}, 200
    else:
        return WRONG_DATA, 400
