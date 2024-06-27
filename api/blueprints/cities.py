
'''
    Cities endpoints:
        '+': Public, '#': Needs auth, '-': Needs is_admin = True.

        +GET /cities: Retrieve all cities.

        +GET /countries/{country_code}/cities: Retrieve all cities belonging to
         a specific country.

        +GET /cities/{city_id}: Retrieve details of a specific city.

        -POST /cities: Create a new city.

        -PUT /cities/{city_id}: Update an existing city's information.

        -DELETE /cities/{city_id}: Delete a specific city.
'''

from flask import request, Blueprint
import api.validations as val
from api.security import notAdmin
from logic import logicexceptions
from logic.logicfacade import LogicFacade
from flask_jwt_extended import jwt_required, get_jwt

bp = Blueprint("cities", __name__, url_prefix="/cities")


@bp.get('/')
def getAllCities():
    """
    Retrieve all cities
    ---
    tags:
      - cities
    responses:
      200:
        description: A list of all cities
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
              name:
                type: string
              country_code:
                type: string
    """

    # Calls BL to get all cities.
    cities = LogicFacade.getByType("city")

    return cities, 200


@bp.get('/<country_code>/cities')
def getCitiesForCountry(country_code):
    """
    Retrieve cities for a specific country
    ---
    tags:
      - cities
    parameters:
      - in: path
        name: country_code
        type: string
        required: true
        description: ISO country code (e.g., 'US' for United States)
    responses:
      200:
        description: A list of cities for the country
      400:
        description: Bad request, invalid country code
      404:
        description: Country not found
    """

    # Check if country code is valid.
    if not val.isCountryValid(country_code):
        return {'error': "Invalid country code"}, 400

    # Call BL to get cities of country.
    try:
        cities = LogicFacade.getContryCities(country_code)
    except (logicexceptions.IDNotFoundError) as err:
        return {'error': str(err)}, 404

    return cities, 200


@bp.get('/<city_id>')
def getCity(city_id):
    """
    Retrieve a city by ID
    ---
    tags:
      - cities
    parameters:
      - in: path
        name: city_id
        type: string
        required: true
        description: The ID of the city to retrieve
    responses:
      200:
        description: City details
      400:
        description: Bad request, invalid ID format
      404:
        description: City not found
    """

    # Check if id is valid.
    if not val.idChecksum(city_id):
        return {'error': "Invalid ID format"}, 400

    # Calls BL to get city.
    try:
        city = LogicFacade.getByID(city_id, "city")
    except (logicexceptions.IDNotFoundError) as err:
        return {'error': str(err)}, 404

    return city, 200


@bp.post('/')
@jwt_required()
def createCity():
    """
    Create a new city
    ---
    tags:
      - cities
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - name
            - country_code
          properties:
            name:
              type: string
              description: The name of the city
              example: New York
            country_code:
              type: string
              description: The ISO code of the country to which the city \
                belongs
              example: US
    responses:
      201:
        description: City created successfully
      400:
        description: Bad request, invalid data or missing fields
      409:
        description: City name already exists
    """

    # Check if user is admin.
    if err := notAdmin(jwt := get_jwt()):
        return err, 403

    # Get data from request.
    data = request.get_json()

    # Check if data is valid.
    if val.isNoneFields('city', data):
        return {'error': "Invalid data"}, 400

    name = data['name']
    code = data['country_code']

    if not (val.isNameValid(name) and
            val.isCountryValid(code)):
        return {'error': "Invalid data"}, 400

    # Calls BL to create city.
    try:
        city = LogicFacade.createObjectByJson("city", data)
    except (logicexceptions.CountryNotFoundError) as err:
        return {'error': str(err)}, 400
    except (logicexceptions.CityNameDuplicated) as err:
        return {'error': str(err)}, 409

    return city, 201


@bp.put('/<city_id>')
@jwt_required()
def updateCity(city_id):
    """
    Update a city by ID
    ---
    tags:
      - cities
    parameters:
      - in: path
        name: city_id
        type: string
        required: true
        description: The ID of the city to update
      - in: body
        name: body
        schema:
          type: object
          required:
            - name
            - country_code
          properties:
            name:
              type: string
              description: The name of the city
              example: Los Angeles
            country_code:
              type: string
              description: The ISO code of the country to which the city \
                belongs
              example: US
    responses:
      200:
        description: City updated successfully
      400:
        description: Bad request, invalid data or ID format
      404:
        description: City not found
      409:
        description: City name already exists
    """

    # Check if user is admin.
    if err := notAdmin(jwt := get_jwt()):
        return err, 403

    # Get data from request.
    data = request.get_json()

    # Check if data is valid.
    if not val.idChecksum(city_id):
        return {'error': "Invalid ID format"}, 400

    if val.isNoneFields('city', data):
        return {'error': "Invalid data"}, 400

    name = data['name']
    code = data['country_code']

    if not val.isNameValid(name) or not val.isCountryValid(code):
        return {'error': "Invalid data"}, 400

    # Calls BL to update city.
    try:
        city = LogicFacade.updateByID(city_id, "city", data)
    except (logicexceptions.CountryNotFoundError) as err:
        return {'error': str(err)}, 400
    except (logicexceptions.IDNotFoundError) as err:
        return {'error': str(err)}, 404
    except (logicexceptions.CityNameDuplicated) as err:
        return {'error': str(err)}, 409

    return city, 201


@bp.delete('/<city_id>')
@jwt_required()
def deleteCity(city_id):
    """
    Delete a city by ID
    ---
    tags:
      - cities
    parameters:
      - in: path
        name: city_id
        type: string
        required: true
        description: The ID of the city to delete
    responses:
      204:
        description: City deleted successfully
      400:
        description: Bad request, invalid ID format
      404:
        description: City not found
    """

    # Check if user is admin.
    if err := notAdmin(jwt := get_jwt()):
        return err, 403

    # Check if id is valid.
    if not val.idChecksum(city_id):
        return {'error': 'Invalid ID'}, 400

    # Calls BL to delete city.
    try:
        LogicFacade.deleteByID(city_id, "city")
    except (logicexceptions.IDNotFoundError) as message:
        return {'error': str(message)}, 404

    return "", 204
