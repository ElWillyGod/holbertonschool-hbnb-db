
'''
    quickdoc
'''

from persistence.country_manager import CountryManager
from logic.model.logicexceptions import CountryNotFoundError

countries = CountryManager.get()


def getCountry(country_code: str):
    '''
        Gets a country object by code.
    '''

    for country in countries:
        if country["code"] == country_code:
            return country

    raise CountryNotFoundError("country not found")


def getCountries():
    '''
        Gets the list of countries.
    '''

    return countries
