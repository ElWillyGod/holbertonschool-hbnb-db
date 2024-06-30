
'''
    Countries endpoints:
        '+': Public, '#': Needs auth, '-': Needs is_admin = True.

        +GET /countries: Retrieve all pre-loaded countries.

        +GET /countries/{country_code}: Retrieve details of a specific country
         by its code.
'''

from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt
from flasgger import swag_from
from logic import logicexceptions
from logic import LogicFacade
import api.validations as val
import api.authlib as authlib

bp = Blueprint("countries", __name__, url_prefix="/countries")


@bp.get('/')
@jwt_required(optional=True)
@swag_from("swagger/countries/get_all.yaml")
def getAllCountries():
    '''
        Gets all countries.
    '''

    # Checks if it's authorized to make the request.
    if err := authlib.notGetAllAuthorized("country", get_jwt()):
        return err, 403

    # Calls BL to get all countries.
    countries = LogicFacade.getAllCountries()

    return countries, 200


@bp.get('/<country_code>')
@jwt_required(optional=True)
@swag_from("swagger/countries/get.yaml")
def getCounty(country_code):
    '''
        Gets a country.
    '''

    # Checks if it's authorized to make the request.
    if err := authlib.notGetAuthorized("country", get_jwt()):
        return err, 403

    # Check if country code is valid.
    if not val.isCountryValid(country_code):
        return {'error': '404 Not Found'}, 404

    # Calls BL to get country.
    try:
        countries = LogicFacade.getCountry(country_code)
    except (logicexceptions.IDNotFoundError) as message:
        return {'error': str(message)}, 404

    return countries, 200
