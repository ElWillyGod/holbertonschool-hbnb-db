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
from logic import logicexceptions
from logic.logicfacade import LogicFacade
import api.validations as val
import api.authlib as authlib

bp = Blueprint("users", __name__, url_prefix="/users")


@bp.get('/')
@jwt_required(optional=False)
def getAllUsers():
    """
    Retrieve details of a specific user.
    ---
    tags:
      - users
    parameters:
      - in: path
        name: user_id
        type: string
        required: true
        description: ID of the user to retrieve
    responses:
      200:
        description: Details of the specified user
    """

    # Checks if it's authorized to make the request.
    if err := authlib.notGetAllAuthorized("user", get_jwt()):
        return err, 403

    # Calls BL to get all users.
    users = LogicFacade.getByType("user")

    return users, 200


@bp.get('/<user_id>')
@jwt_required(optional=False)
def getUser(user_id):
    """
    Update an existing user.
    ---
    tags:
      - users
    parameters:
      - in: path
        name: user_id
        type: string
        required: true
        description: ID of the user to update
      - in: body
        name: user
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              description: Updated email address of the user
            first_name:
              type: string
              description: Updated first name of the user
            last_name:
              type: string
              description: Updated last name of the user
    responses:
      201:
        description: User updated successfully
      400:
        description: Invalid request data or missing fields
      404:
        description: User ID not found
    """

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
def createUser():
    """
    Create a new user.
    ---
    tags:
      - users
    parameters:
      - in: body
        name: user
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              description: Email address of the user
            first_name:
              type: string
              description: First name of the user
            last_name:
              type: string
              description: Last name of the user
    responses:
      201:
        description: User created successfully
      400:
        description: Invalid request data or missing fields
      409:
        description: Email address already exists
    """

    # Checks if it's authorized to make the request.
    if err := authlib.notPostAuthorized("user", get_jwt()):
        return err, 403

    # Get data from request.
    data = request.get_json()

    # Check if data is valid.
    if val.isNoneFields('user', data):
        return {'error': "Invalid data or missing fields"}, 400

    email = data.get('email')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    if (not val.isStrValid(email) or
            not val.isNameValid(first_name) or
            not val.isNameValid(last_name)):
        return {'error': "Invalid data or missing fields"}, 400

    if not val.isEmailValid(email):
        return {'error': "Invalid data"}, 400

    # Calls BL to create user.
    try:
        user = LogicFacade.createObjectByJson("user", data)
    except (logicexceptions.EmailDuplicated) as err:
        return {'error': str(err)}, 409

    return user, 201


@bp.put('/<user_id>')
@jwt_required(optional=False)
def updateUser(user_id):
    """
    Update an existing user.
    ---
    tags:
      - users
    parameters:
      - in: path
        name: user_id
        type: string
        required: true
        description: ID of the user to update
      - in: body
        name: user
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              description: Updated email address of the user
              example: juanpepe@gmail.com
            first_name:
              type: string
              description: Updated first name of the user
              example: juan
            last_name:
              type: string
              description: Updated last name of the user
              example: pepe
    responses:
      201:
        description: User updated successfully
      400:
        description: Invalid request data or missing fields
      404:
        description: User ID not found
      409:
        description: Email address already exists
    """

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

    if (not val.isStrValid(email) or
            not val.isNameValid(first_name) or
            not val.isNameValid(last_name)):
        return {'error': "Invalid data or missing fields"}, 400

    if not val.isEmailValid(email):
        return {'error': "Invalid email"}, 400

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
def deleteUser(user_id):
    """
    Delete a user.
    ---
    tags:
      - users
    parameters:
      - in: path
        name: user_id
        type: string
        required: true
        description: ID of the user to delete
    responses:
      204:
        description: User deleted successfully
      400:
        description: Invalid user ID format
      404:
        description: User ID not found
    """

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
