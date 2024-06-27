
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


# @jwt_required()
#    if err := notAdmin(jwt := get_jwt()):
#        return err, 403


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
    if not val.idChecksum(amenity_id):
        return {'error': "Invalid ID"}, 400

    try:
        amenities = LogicFacade.getByID(amenity_id, 'amenity')

    except (logicexceptions.IDNotFoundError) as message:
        return {'error': str(message)}, 404

    return amenities, 200


@bp.post('/')
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
    data = request.get_json()

    if val.isNoneFields('amenity', data) or not val.isNameValid(data['name']):
        return {'error': "Invalid data"}, 400

    try:
        amenity = LogicFacade.createObjectByJson('amenity', data)

    except (logicexceptions.AmenityNameDuplicated) as message:
        return {'error': str(message)}, 409

    return amenity, 201


@bp.put('/<amenity_id>')
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
    data = request.get_json()

    if val.isNoneFields('amenity', data) or not val.isNameValid(data['name']):
        return {'error': "Invalid data"}, 400

    if not val.idChecksum(amenity_id):
        return {'error': 'Invalid ID format'}, 400

    try:
        amenity = LogicFacade.updateByID(amenity_id, 'amenity', data)

    except (logicexceptions.AmenityNameDuplicated) as message:
        return {'error': str(message)}, 409

    except (logicexceptions.IDNotFoundError) as message2:
        return {'error': str(message2)}, 404

    return amenity, 201


@bp.delete('/<amenity_id>')
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
    if not val.idChecksum(amenity_id):
        return {'message': "Invalid ID format"}, 400

    try:
        LogicFacade.deleteByID(amenity_id, 'amenity')

    except (logicexceptions.IDNotFoundError) as message:
        return {'error': str(message)}, 404

    return "", 204
