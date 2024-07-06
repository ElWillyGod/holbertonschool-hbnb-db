
'''
    Places endpoints:
        '+': Public, '#': Needs auth, '@': Needs auth and be the same user
             that created it, '-': Needs is_admin = True.

        +GET /places: Retrieve a list of all places.

        +GET /places/{place_id}: Retrieve detailed information about a specific
         place.

        #POST /places: Create a new place.

        @PUT /places/{place_id}: Update an existing place's information.

        @DELETE /places/{place_id}: Delete a specific place.
    TODO: 409 does not get raise on POST and PUT
'''

from flask import request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt
from flasgger import swag_from
from logic import logicexceptions
from logic.logicfacade import LogicFacade
import api.validations as val
import api.authlib as authlib
from werkzeug.exceptions import BadRequest, Forbidden, Conflict, NotFound

bp = Blueprint("places", __name__, url_prefix="/places")


@bp.get('/')
@jwt_required(optional=True)
@swag_from("swagger/places/get_all.yaml")
def getAllPlaces():
    '''
        Gets all places.
    '''

    # Checks if it's authorized to make the request.
    if err := authlib.notGetAllAuthorized("place", get_jwt()):
        raise Forbidden(err)

    # Calls BL to get all places.
    places = LogicFacade.getByType('place')

    return places, 200


@bp.get('/<place_id>')
@jwt_required(optional=True)
@swag_from("swagger/places/get.yaml")
def getPlace(place_id):
    '''
        Gets place.
    '''

    # Checks if it's authorized to make the request.
    if err := authlib.notGetAuthorized("place", get_jwt()):
        raise Forbidden(err)

    # Check if id is valid.
    if not val.idChecksum(place_id):
        raise BadRequest("invalid id")

    # Calls BL to get place.
    try:
        place = LogicFacade.getByID(place_id, 'place')
    except (logicexceptions.IDNotFoundError) as err:
        raise NotFound(str(err))

    return place, 200


@bp.post('/')
@jwt_required(optional=False)
@swag_from("swagger/places/post.yaml")
def createPlace():
    '''
        Creates a place.
    '''

    # Checks if it's authorized to make the request.
    if err := authlib.notPostAuthorized("place", get_jwt()):
        raise Forbidden(err)

    # Get data from request.
    data = request.get_json()

    # Check if data is valid.
    if val.isNoneFields('place', data):
        raise BadRequest("invalid data")

    if not val.idChecksum(data['host_id']):
        raise BadRequest("invalid host id")

    if not val.idChecksum(data['city_id']):
        raise BadRequest("invalid city id")

    if not (val.isLatitudeValid(data['latitude']) and
            val.isLongitudeValid(data['longitude'])):
        raise BadRequest("invalid location")

    if not val.isNameValid(data['name']):
        raise BadRequest("invalid name")

    if not (isinstance(data['number_of_rooms'], int) and
            isinstance(data['number_of_bathrooms'], int) and
            isinstance(data['max_guests'], int) and
            isinstance(data['price_per_night'], (int, float))):
        raise BadRequest("invalid data")

    if not (data['number_of_rooms'] > 0 and
            data['number_of_bathrooms'] >= 0 and
            data['max_guests'] > 0 and
            data['price_per_night'] > 0):
        raise BadRequest("invalid data")

    for amenity_id in data['amenity_ids']:
        if not val.idChecksum(amenity_id):
            raise BadRequest(f'invalid amenity id: {amenity_id}')

    # Calls BL to create place.
    try:
        place = LogicFacade.createObjectByJson('place', data)
    except (logicexceptions.IDNotFoundError) as err:
        raise NotFound(str(err))

    return place, 201


@bp.put('/<place_id>')
@jwt_required(optional=False)
@swag_from("swagger/places/put.yaml")
def updatePlace(place_id):
    '''
        Updates a place.
    '''

    # Checks if it's authorized to make the request.
    if err := authlib.notPutAuthorized("place", get_jwt()):
        raise Forbidden(err)

    # Get data from request.
    data = request.get_json()

    # Check if data is valid.
    if not val.idChecksum(place_id):
        raise BadRequest("invalid id")

    if val.isNoneFields('place', data):
        raise BadRequest("invalid data")

    if not (val.isLatitudeValid(data['latitude']) and
            val.isLongitudeValid(data['longitude'])):
        raise BadRequest("invalid location")

    if not (isinstance(data['number_of_rooms'], int) and
            isinstance(data['number_of_bathrooms'], int) and
            isinstance(data['max_guests'], int) and
            isinstance(data['price_per_night'], (int, float))):
        raise BadRequest("invalid data")

    if not (data['number_of_rooms'] > 0 and
            data['number_of_bathrooms'] >= 0 and
            data['max_guests'] > 0 and
            data['price_per_night'] > 0):
        raise BadRequest("invalid data")

    if not val.idChecksum(data['city_id']):
        raise BadRequest("invalid city id")

    for amenity_id in data['amenity_ids']:
        if not val.idChecksum(amenity_id):
            raise BadRequest('invalid amenity id')

    # Calls BL to update place.
    try:
        place = LogicFacade.updateByID(place_id, 'place', data)
    except (logicexceptions.IDNotFoundError) as err:
        raise NotFound(str(err))

    return place, 200


@bp.delete('/<place_id>')
@jwt_required(optional=False)
@swag_from("swagger/places/delete.yaml")
def deletePlace(place_id):
    '''
        Deletes a place.
    '''

    # Checks if it's authorized to make the request.
    if err := authlib.notDeleteAuthorized("place", get_jwt()):
        raise Forbidden(err)

    # Check if id is valid.
    if not val.idChecksum(place_id):
        raise BadRequest("invalid place id")

    # Calls BL to delete place.
    try:
        LogicFacade.deleteByID(place_id, 'place')
    except (logicexceptions.IDNotFoundError) as err:
        raise NotFound(str(err))

    return "", 204
