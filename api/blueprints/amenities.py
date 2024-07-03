
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
from flask_jwt_extended import jwt_required, get_jwt
from flasgger import swag_from
from logic import logicexceptions
from logic.logicfacade import LogicFacade
import api.validations as val
import api.authlib as authlib
from werkzeug.exceptions import BadRequest, Forbidden, Conflict, NotFound

bp = Blueprint("amenities", __name__, url_prefix="/amenities")


@bp.get('/')
@jwt_required(optional=True)
@swag_from("swagger/amenities/get_all.yaml")
def getAllAmenities():
    """
        Gets all amenities.
    """

    # Checks if it's authorized to make the request.
    if err := authlib.notGetAllAuthorized("amenity", get_jwt()):
        raise Forbidden(err)

    # Calls BL to get all amenities
    amenities = LogicFacade.getByType('amenity')

    return amenities, 200


@bp.get('/<amenity_id>')
@jwt_required(optional=True)
@swag_from("swagger/amenities/get.yaml")
def getAmenity(amenity_id):
    """
        Get an amenity.
    """

    # Checks if it's authorized to make the request.
    if err := authlib.notGetAuthorized("amenity", get_jwt()):
        raise Forbidden(err)

    # Checks if id is valid.
    if not val.idChecksum(amenity_id):
        raise BadRequest("invalid id")

    # Calls BL to get amenity
    try:
        amenities = LogicFacade.getByID(amenity_id, 'amenity')
    except (logicexceptions.IDNotFoundError) as err:
        raise NotFound(str(err))

    return amenities, 200


@bp.post('/')
@jwt_required(optional=False)
@swag_from("swagger/amenities/post.yaml")
def createAmenity():
    """
        Creates an amenity.
    """

    # Checks if it's authorized to make the request.
    if err := authlib.notPostAuthorized("amenity", get_jwt()):
        raise Forbidden(err)

    # Get data from request.
    data = request.get_json()

    # Check if data is valid.
    if (val.isNoneFields('amenity', data) or
            not val.isNameValid(data['name'])):
        raise BadRequest("invalid data")

    # Try creating amenity in BL layer.
    try:
        amenity = LogicFacade.createObjectByJson('amenity', data)
    except (logicexceptions.AmenityNameDuplicated) as err:
        raise Conflict(str(err))

    return amenity, 201


@bp.put('/<amenity_id>')
@jwt_required(optional=False)
@swag_from("swagger/amenities/put.yaml")
def updateAmenity(amenity_id):
    """
        Updates an amenity.
    """

    # Checks if it's authorized to make the request.
    if err := authlib.notPutAuthorized("amenity", get_jwt()):
        raise Forbidden(err)

    # Get data from request.
    data = request.get_json()

    # Check if data is valid.
    if val.isNoneFields('amenity', data) or not val.isNameValid(data['name']):
        raise BadRequest("invalid data")

    if not val.idChecksum(amenity_id):
        raise BadRequest('invalid id format')

    # Try updating amenity in BL layer.
    try:
        amenity = LogicFacade.updateByID(amenity_id, 'amenity', data)
    except (logicexceptions.AmenityNameDuplicated) as err:
        raise Conflict(str(err))
    except (logicexceptions.IDNotFoundError) as err:
        raise NotFound(str(err))

    return amenity, 204


@bp.delete('/<amenity_id>')
@jwt_required(optional=False)
@swag_from("swagger/amenities/delete.yaml")
def deleteAmenity(amenity_id):
    """
        Deletes an amenity.
    """

    # Checks if it's authorized to make the request.
    if err := authlib.notDeleteAuthorized("amenity", get_jwt()):
        raise Forbidden(err)

    # Try creating amenity in BL layer.
    if not val.idChecksum(amenity_id):
        raise BadRequest("invalid id format")

    # Try creating amenity in BL layer.
    try:
        LogicFacade.deleteByID(amenity_id, 'amenity')
    except (logicexceptions.IDNotFoundError) as err:
        raise NotFound(str(err))

    return "", 204
