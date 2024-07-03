
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
from logic.logicfacade import LogicFacade
import api.validations as val
import api.authlib as authlib
from werkzeug.exceptions import BadRequest, Forbidden, NotFound

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
        raise Forbidden(err)

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
        raise Forbidden(err)

    # Check if country code is valid.
    if not val.isCountryValid(country_code):
        raise BadRequest('code is not valid')

    # Calls BL to get country.
    try:
        countries = LogicFacade.getCountry(country_code)
    except (logicexceptions.CountryNotFoundError) as err:
        raise NotFound(str(err))

    return countries, 200
