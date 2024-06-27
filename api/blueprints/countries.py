
'''
    Countries endpoints:

        -GET /countries: Retrieve all pre-loaded countries.

        -GET /countries/{country_code}: Retrieve details of a specific country
         by its code.
'''

from logic import logicexceptions, Blueprint
import api.validations as val
from logic.logicfacade import LogicFacade

bp = Blueprint("countries", __name__, url_prefix="/countries")


@bp.get('/')
def get_All_Countries():
    """
    Retrieve all countries
    ---
    tags:
      - countries
    responses:
      200:
        description: A list of all countries
    """
    countries = LogicFacade.getAllCountries()

    return countries, 200


@bp.get('/<country_code>')
def get_Countries(country_code):
    """
    Retrieve details of a specific country by its code
    ---
    tags:
      - countries
    parameters:
      - in: path
        name: country_code
        type: string
        required: true
        description: ISO code of the country (e.g., 'US' for United States)
    responses:
      200:
        description: All countries retrieved
      404:
        description: Country not found
    """

    if not val.isCountryValid(country_code):
        return {'error': '404 Not Found'}, 404

    try:
        countries = LogicFacade.getCountry(country_code)

    except (logicexceptions.IDNotFoundError) as message:
        
        return {'error': str(message)}, 404

    return countries, 200
