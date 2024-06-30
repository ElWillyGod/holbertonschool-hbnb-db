
'''
    Users endpoints:
        '+': Public, '#': Needs auth, '-': Needs is_admin = True.

        -GET /users: Retrieve a list of all users.

        -GET /users/{user_id}: Retrieve details of a specific user.

        -POST /users: Create a new user.

        -PUT /users/{user_id}: Update an existing user.

        -DELETE /users/{user_id}: Delete a user.
'''

from flask import request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt
from flasgger import swag_from
from logic import logicexceptions
from logic.logicfacade import LogicFacade
from api.security import hashPassword
import api.validations as val
import api.authlib as authlib

bp = Blueprint("users", __name__, url_prefix="/users")


@bp.get('/')
@jwt_required(optional=False)
@swag_from("swagger/users/get_all.yaml")
def getAllUsers():
    '''
        Gets all users.
    '''

    # Checks if it's authorized to make the request.
    if err := authlib.notGetAllAuthorized("user", get_jwt()):
        return err, 403

    # Calls BL to get all users.
    users = LogicFacade.getByType("user")

    return users, 200


@bp.get('/<user_id>')
@jwt_required(optional=False)
@swag_from("swagger/users/get.yaml")
def getUser(user_id):
    '''
        Gets a user.
    '''

    # Checks if it's authorized to make the request.
    if err := authlib.notGetAuthorized("user", get_jwt()):
        return err, 403

    # Checks if id is valid.
    if not val.idChecksum(user_id):
        return {'error': "Invalid data"}, 400

    # Calls BL to get user.
    try:
        users = LogicFacade.getByID(user_id, 'user')
    except (logicexceptions.IDNotFoundError) as err:
        return {'error': str(err)}, 404

    return users, 200


@bp.post("/")
@jwt_required(optional=False)
@swag_from("swagger/users/post.yaml")
def createUser():
    '''
        Creates a user.
    '''

    # Checks if it's authorized to make the request.
    if err := authlib.notPostAuthorized("user", get_jwt()):
        return err, 403

    # Get data from request.
    data = request.get_json()

    # Check if data is valid.
    if val.isNoneFields('user', data):
        return {'error': "Invalid data or missing fields"}, 400

    email = data.get('email', "email")
    first_name = data.get('first_name', "firstname")
    last_name = data.get('last_name', "lastname")
    password = data.get('password', "password")
    is_admin = data.get('is_admin', False)

    if (not val.isStrValid(email) or
            not val.isNameValid(first_name) or
            not val.isNameValid(last_name)):
        return {'error': "Invalid data or missing fields"}, 400

    if not val.isEmailValid(email):
        return {'error': "Invalid data"}, 400

    if not val.isPasswordValid(password):
        return {'error': "invalid password"}, 400

    if not isinstance(is_admin, bool):
        return {'error': "invalid is_admin"}, 400

    # Hashes password.
    data["password"] = hashPassword(data["password"])

    # Calls BL to create user.
    try:
        user = LogicFacade.createObjectByJson("user", data)
    except (logicexceptions.EmailDuplicated) as err:
        return {'error': str(err)}, 409

    return user, 201


@bp.put('/<user_id>')
@jwt_required(optional=False)
@swag_from("swagger/users/put.yaml")
def updateUser(user_id):
    '''
        Updates a user.
    '''

    # Checks if it's authorized to make the request.
    if err := authlib.notPutAuthorized("user", get_jwt()):
        return err, 403

    # Checks if id is valid.
    if not val.idChecksum(user_id):
        return {'error': 'Invalid id'}, 400

    # Get data from request.
    data = request.get_json()

    # Checks if data is valid.
    if val.isNoneFields('user', data):
        return {'error': "Invalid data"}, 400

    email = data.get('email')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    password = data.get('password', "password")
    is_admin = data.get('is_admin', False)

    if (not val.isStrValid(email) or
            not val.isNameValid(first_name) or
            not val.isNameValid(last_name)):
        return {'error': "invalid data"}, 400

    if not val.isEmailValid(email):
        return {'error': "invalid email"}, 400

    if not val.isPasswordValid(password):
        return {'error': "invalid password"}, 400

    if not isinstance(is_admin, bool):
        return {'error': "invalid is_admin"}, 400

    # Hashes password.
    data["password"] = hashPassword(data["password"])

    # Calls BL to update user.
    try:
        user = LogicFacade.updateByID(user_id, "user", data, user=get_jwt())
    except (logicexceptions.EmailDuplicated) as err:
        return {'error': str(err)}, 409
    except (logicexceptions.IDNotFoundError) as err:
        return {'error': str(err)}, 404

    return user, 201


@bp.delete('/<user_id>')
@jwt_required(optional=False)
@swag_from("swagger/users/delete.yaml")
def deleteUser(user_id):
    '''
        Deletes a user.
    '''

    # Checks if it's authorized to make the request.
    if err := authlib.notDeleteAuthorized("user", get_jwt()):
        return err, 403

    # Checks if id is valid.
    if not val.idChecksum(user_id):
        return {'error': 'Invalid user ID'}, 400

    # Calls BL to delete user.
    try:
        LogicFacade.deleteByID(user_id, "user", user=get_jwt())
    except (logicexceptions.IDNotFoundError) as err:
        return {'error': str(err)}, 404

    return "", 204
