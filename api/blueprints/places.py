
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
'''

from flask import request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt
from flasgger import swag_from
from logic import logicexceptions
from logic import LogicFacade
import api.validations as val
import api.authlib as authlib

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
        return err, 403

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
        return err, 403

    # Check if id is valid.
    if not val.idChecksum(place_id):
        return {'err': "Invalid ID"}, 400

    # Calls BL to get place.
    try:
        place = LogicFacade.getByID(place_id, 'place')
    except (logicexceptions.IDNotFoundError) as err:
        return {'error': str(err)}, 404

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
        return err, 403

    # Get data from request.
    data = request.get_json()

    # Check if data is valid.
    if val.isNoneFields('place', data):
        return {'error': "Invalid data"}, 400

    if not val.idChecksum(data['host_id']):
        return {'error': "Invalid host ID"}, 400

    if not val.idChecksum(data['city_id']):
        return {'error': "Invalid city ID"}, 400

    if not (val.isLatitudeValid(data['latitude']) and
            val.isLongitudeValid(data['longitude'])):
        return {'error': "Invalid location"}, 400

    if not val.isNameValid(data['name']):
        return {'error': "Invalid name"}, 400

    if not (isinstance(data['number_of_rooms'], int) and
            isinstance(data['number_of_bathrooms'], int) and
            isinstance(data['max_guests'], int) and
            isinstance(data['price_per_night'], (int, float))):
        return {'error': "Invalid data"}, 400

    if not (data['number_of_rooms'] > 0 and
            data['number_of_bathrooms'] >= 0 and
            data['max_guests'] > 0 and
            data['price_per_night'] > 0):
        return {'error': "Invalid data"}, 400

    for amenity_id in data['amenity_ids']:
        if not val.idChecksum(amenity_id):
            return {'error': f'Invalid amenity ID: {amenity_id}'}, 400

    # Calls BL to create place.
    try:
        place = LogicFacade.createObjectByJson('place', data)
    except (logicexceptions.IDNotFoundError) as err:
        return {'error': str(err)}, 404

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
        return err, 403

    # Get data from request.
    data = request.get_json()

    # Check if data is valid.
    if not val.idChecksum(place_id):
        return {'error': "Invalid ID"}, 400

    if val.isNoneFields('place', data):
        return {'error': "Invalid data"}, 400

    if not (val.isLatitudeValid(data['latitude']) and
            val.isLongitudeValid(data['longitude'])):
        return {'error': "Invalid location"}, 400

    if not (isinstance(data['number_of_rooms'], int) and
            isinstance(data['number_of_bathrooms'], int) and
            isinstance(data['max_guests'], int) and
            isinstance(data['price_per_night'], (int, float))):
        return {'error': "Invalid data"}, 400

    if not (data['number_of_rooms'] > 0 and
            data['number_of_bathrooms'] >= 0 and
            data['max_guests'] > 0 and
            data['price_per_night'] > 0):
        return {'error': "Invalid data"}, 400

    if not val.idChecksum(data['city_id']):
        return {'error': "Invalid city ID"}, 400

    for amenity_id in data['amenity_ids']:
        if not val.idChecksum(amenity_id):
            return {'error': 'Invalid amenity ID'}, 400

    # Calls BL to update place.
    try:
        place = LogicFacade.updateByID(place_id, 'place', data)
    except (logicexceptions.IDNotFoundError) as err:
        return {'error': str(err)}, 404

    return place, 201


@bp.delete('/<place_id>')
@jwt_required(optional=False)
@swag_from("swagger/places/delete.yaml")
def deletePlace(place_id):
    '''
        Deletes a place.
    '''

    # Checks if it's authorized to make the request.
    if err := authlib.notDeleteAuthorized("place", get_jwt()):
        return err, 403

    # Check if id is valid.
    if not val.idChecksum(place_id):
        return {'error': "Invalid place ID"}, 400

    # Calls BL to delete place.
    try:
        LogicFacade.deleteByID(place_id, 'place')
    except (logicexceptions.IDNotFoundError) as err:
        return {'error': str(err)}, 404

    return "", 204
