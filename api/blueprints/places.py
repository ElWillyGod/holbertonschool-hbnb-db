
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
import api.validations as val
from api.security import notAdmin
from logic import logicexceptions
from logic.logicfacade import LogicFacade
from flask_jwt_extended import jwt_required, get_jwt

bp = Blueprint("places", __name__, url_prefix="/places")


@bp.get('/')
def getAllPlaces():
    """
    Retrieve all places
    ---
    tags:
      - places
    responses:
      200:
        description: A list of all places
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
                description: The ID of the place
              name:
                type: string
                description: The name of the place
              description:
                type: string
                description: Description of the place
              city_id:
                type: string
                description: ID of the city where the place is located
              host_id:
                type: string
                description: ID of the host of the place
              amenities:
                type: array
                items:
                  type: string
                description: List of amenity IDs available at the place
              created_at:
                type: string
                description: Date and time when the place was created
              updated_at:
                type: string
                description: Date and time when the place was last updated
    """

    # Calls BL to get all places.
    places = LogicFacade.getByType('place')

    return places, 200


@bp.get('/<place_id>')
def getPlace(place_id):
    """
    Retrieve details of a specific place by its ID
    ---
    tags:
      - places
    parameters:
      - in: path
        name: place_id
        type: string
        required: true
        description: ID of the place
    responses:
      200:
        description: Details of the place
        schema:
          type: object
          properties:
            id:
              type: string
              description: The ID of the place
            name:
              type: string
              description: The name of the place
            description:
              type: string
              description: Description of the place
            city_id:
              type: string
              description: ID of the city where the place is located
            host_id:
              type: string
              description: ID of the host of the place
            amenities:
              type: array
              items:
                type: string
              description: List of amenity IDs available at the place
            created_at:
              type: string
              description: Date and time when the place was created
            updated_at:
              type: string
              description: Date and time when the place was last updated
      400:
        description: Invalid place ID format
      404:
        description: Place not found
    """

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
@jwt_required()
def createPlace():
    """
    Create a new place
    ---
    tags:
      - places
    parameters:
      - in: body
        name: place
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              description: The name of the place
              example: Casa de playa
            description:
              type: string
              description: Description of the place
              example: es una casa en la playa
            city_id:
              type: string
              description: ID of the city where the place is located
            host_id:
              type: string
              description: ID of the host of the place
            amenity_ids:
              type: array
              items:
                type: string
              description: List of amenity IDs available at the place
    responses:
      201:
        description: Place created successfully
      400:
        description: Invalid request data or missing fields
      404:
        description: City ID not found
    """

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
@jwt_required()
def updatePlace(place_id):
    """
    Update an existing place's information
    ---
    tags:
      - places
    parameters:
      - in: path
        name: place_id
        type: string
        required: true
        description: ID of the place to be updated
      - in: body
        name: place
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              description: The name of the place
            description:
              type: string
              description: Description of the place
            city_id:
              type: string
              description: ID of the city where the place is located
            host_id:
              type: string
              description: ID of the host of the place
            amenity_ids:
              type: array
              items:
                type: string
              description: List of amenity IDs available at the place
    responses:
      200:
        description: Place updated successfully
      400:
        description: Invalid request data or missing fields
      404:
        description: Place ID not found
    """

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
    # If admin it can update places of other people.
    is_admin: bool = get_jwt().get("is_admin", False)
    try:
        place = LogicFacade.updateByID(
            place_id, 'place', data, is_admin=is_admin)
    except (logicexceptions.IDNotFoundError) as err:
        return {'error': str(err)}, 404

    return place, 201


@bp.delete('/<place_id>')
@jwt_required()
def deletePlace(place_id):
    """
    Delete a specific place by its ID
    ---
    tags:
      - places
    parameters:
      - in: path
        name: place_id
        type: string
        required: true
        description: ID of the place to be deleted
    responses:
      204:
        description: Place deleted successfully
      400:
        description: Invalid place ID format
      404:
        description: Place not found
    """

    # Check if id is valid.
    if not val.idChecksum(place_id):
        return {'error': "Invalid place ID"}, 400

    # Calls BL to delete place.
    # If admin it can deletes places of other people.
    is_admin: bool = get_jwt().get("is_admin", False)
    try:
        LogicFacade.deleteByID(place_id, 'place', is_admin=is_admin)
    except (logicexceptions.IDNotFoundError) as err:
        return {'error': str(err)}, 404

    return "", 204


'''
    for place in places:

        city = getCity(place['city_id'])
        amenities = [getAmenity(amenity_id) for amenity_id in \
            place['amenity_ids']]
        response.append({
            'id': place['id'],
            'name': place['name'],
            'description': place['description'],
            'address': place['address'],
            'city_id': place['city_id'],
            'latitude': place['latitude'],
            'longitude': place['longitude'],
            'host_id': place['host_id'],
            'number_of_rooms': place['number_of_rooms'],
            'number_of_bathrooms': place['number_of_bathrooms'],
            'price_per_night': place['price_per_night'],
            'max_guests': place['max_guests'],
            'city': city,
            'amenities': amenities,
            'created_at': place['created_at'],
            'updated_at': place['updated_at']
            })
            '''