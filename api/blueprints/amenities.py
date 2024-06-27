
'''
    Amenities endpoints:
        '+': Public, '#': Needs auth, '-': Needs is_admin = True.

        +GET /amenities/{amenity_id}: Retrieve detailed information about a
         specific amenity.

        +GET /amenities: Retrieve a list of all amenities.

        -POST /amenities: Create a new amenity.

        -PUT /amenities/{amenity_id}: Update an existing amenity's information.

        -DELETE /amenities/{amenity_id}: Delete a specific amenity.
'''

from flask import request, Blueprint
import api.validations as val
from api.security import notAdmin
from logic import logicexceptions
from logic.logicfacade import LogicFacade
from flask_jwt_extended import jwt_required, get_jwt

bp = Blueprint("amenities", __name__, url_prefix="/amenities")


@bp.get('/')
def getAllAmenities():
    """
    Retrieve a list of all amenities
    ---
    tags:
      - amenities
    responses:
      200:
        description: A list of amenities
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
              name:
                type: string
              created_at:
                type: string
              updated_at:
                type: string
      200:
        description: No amenities found
    """

    # Calls BL to get all amenities
    amenities = LogicFacade.getByType('amenity')

    return amenities, 200


@bp.get('/<amenity_id>')
def getAmenity(amenity_id):
    """
    Retrieve an amenity by ID
    ---
    tags:
      - amenities
    parameters:
      - in: path
        name: amenity_id
        type: string
        required: true
        description: The ID of the amenity to retrieve
    responses:
      200:
        description: Amenity details
      400:
        description: Bad request, invalid ID format
      404:
        description: Amenity not found
    """

    # Checks if id is valid.
    if not val.idChecksum(amenity_id):
        return {'error': "Invalid ID"}, 400

    # Calls BL to get amenity
    try:
        amenities = LogicFacade.getByID(amenity_id, 'amenity')
    except (logicexceptions.IDNotFoundError) as error:
        return {'error': str(error)}, 404

    return amenities, 200


@bp.post('/')
@jwt_required()
def createAmenity():
    """
    Create a new amenity
    ---
    tags:
      - amenities
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
              description: The name of the amenity
              example: Pool
    responses:
      201:
        description: Amenity created successfully
      400:
        description: Bad request, invalid data
      409:
        description: Amenity name already exists
    """

    # Check if user is admin.
    if err := notAdmin(jwt := get_jwt()):
        return err, 403

    # Get data from request.
    data = request.get_json()

    # Check if data is valid.
    if (val.isNoneFields('amenity', data) or
            not val.isNameValid(data['name'])):
        return {'error': "Invalid data"}, 400

    # Try creating amenity in BL layer.
    try:
        amenity = LogicFacade.createObjectByJson('amenity', data)
    except (logicexceptions.AmenityNameDuplicated) as error:
        return {'error': str(error)}, 409

    return amenity, 201


@bp.put('/<amenity_id>')
@jwt_required()
def updateAmenity(amenity_id):
    """
    Update an amenity by ID
    ---
    tags:
      - amenities
    parameters:
      - in: path
        name: amenity_id
        type: string
        required: true
        description: The ID of the amenity to update
      - in: body
        name: body
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
              description: The name of the amenity
              example: Gym
    responses:
      200:
        description: Amenity updated successfully
      400:
        description: Bad request, invalid data or ID format
      404:
        description: Amenity not found
      409:
        description: Amenity name already exists
    """

    # Check if user is admin.
    if err := notAdmin(jwt := get_jwt()):
        return err, 403

    # Get data from request.
    data = request.get_json()

    # Check if data is valid.
    if val.isNoneFields('amenity', data) or not val.isNameValid(data['name']):
        return {'error': "Invalid data"}, 400

    if not val.idChecksum(amenity_id):
        return {'error': 'Invalid ID format'}, 400

    # Try updating amenity in BL layer.
    try:
        amenity = LogicFacade.updateByID(amenity_id, 'amenity', data)
    except (logicexceptions.AmenityNameDuplicated) as err:
        return {'error': str(err)}, 409
    except (logicexceptions.IDNotFoundError) as err:
        return {'error': str(err)}, 404

    return amenity, 201


@bp.delete('/<amenity_id>')
@jwt_required()
def deleteAmenity(amenity_id):
    """
    Delete an amenity by ID
    ---
    tags:
      - amenities
    parameters:
      - in: path
        name: amenity_id
        type: string
        required: true
        description: The ID of the amenity to delete
    responses:
      204:
        description: Amenity deleted successfully
      400:
        description: Bad request, invalid ID format
      404:
        description: Amenity not found
    """

    # Check if user is admin.
    if err := notAdmin(jwt := get_jwt()):
        return err, 403

    # Try creating amenity in BL layer.
    if not val.idChecksum(amenity_id):
        return {'error': "Invalid ID format"}, 400

    # Try creating amenity in BL layer.
    try:
        LogicFacade.deleteByID(amenity_id, 'amenity')
    except (logicexceptions.IDNotFoundError) as err:
        return {'error': str(err)}, 404

    return "", 204
