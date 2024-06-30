
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
from flask_jwt_extended import jwt_required, get_jwt
from flasgger import swag_from
from logic import logicexceptions
from logic.logicfacade import LogicFacade
import api.validations as val
import api.authlib as authlib

bp = Blueprint("cities", __name__, url_prefix="/cities")


@bp.get('/')
@jwt_required(optional=True)
@swag_from("swagger/cities/get_all.yaml")
def getAllCities():
    '''
        Gets all cities.
    '''

    # Checks if it's authorized to make the request.
    if err := authlib.notGetAllAuthorized("city", get_jwt()):
        return err, 403

    # Calls BL to get all cities.
    cities = LogicFacade.getByType("city")

    return cities, 200


@bp.get('/<country_code>/cities')
@jwt_required(optional=True)
@swag_from("swagger/cities/country_get_all.yaml")
def getCitiesForCountry(country_code):
    '''
        Gets all cities from country.
    '''

    # Checks if it's authorized to make the request.
    if err := authlib.notGetAllAuthorized("country/city", get_jwt()):
        return err, 403

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
@jwt_required(optional=True)
@swag_from("swagger/cities/get.yaml")
def getCity(city_id):
    '''
        Gets a city.
    '''

    # Checks if it's authorized to make the request.
    if err := authlib.notGetAuthorized("city", get_jwt()):
        return err, 403

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
@jwt_required(optional=False)
@swag_from("swagger/cities/post.yaml")
def createCity():
    '''
        Creates a city.
    '''

    # Checks if it's authorized to make the request.
    if err := authlib.notPostAuthorized("city", get_jwt()):
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
@jwt_required(optional=False)
@swag_from("swagger/cities/put.yaml")
def updateCity(city_id):
    '''
        Updates a city.
    '''

    # Checks if it's authorized to make the request.
    if err := authlib.notPutAuthorized("city", get_jwt()):
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
@jwt_required(optional=False)
@swag_from("swagger/cities/delete.yaml")
def deleteCity(city_id):
    '''
        Deletes a city.
    '''

    # Checks if it's authorized to make the request.
    if err := authlib.notDeleteAuthorized("city", get_jwt()):
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
