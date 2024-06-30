
'''
    quickdoc
'''

from persistence.country_manager import CountryManager

countries = CountryManager.get()


def getCountry(country_code: str):
    '''
        Gets a country object by code.
    '''

    for country in countries:
        if country["code"] == country_code:
            return country

    raise Exception("country not found")


def getCountries():
    '''
        Gets the list of countries.
    '''

    return countries
