
'''
    Defines validation functions.
    Makes calls to the persistance layer.
'''

from persistence import dm
from logic.model.countrieslib import getCountries


def idExists(id: str, cls: str) -> bool:
    '''
        Calls persistance layer to see if an id of type cls exists.
    '''

    call = dm.get(id, cls)

    if call is None or len(call) == 0:
        return False

    return True


def isUserEmailDuplicated(email: str) -> bool:
    '''
        Calls persistance layer to see if a user has the same email.
    '''

    call = dm.get_by_property("users", "email", email)

    if call is None or len(call) == 0:
        return False

    return True


def isAmenityDuplicated(name: str) -> bool:
    '''
        Calls persistance layer to see if a user has the same email.
    '''

    call = dm.get_by_property("amenities", "name", name)

    if call is None or len(call) == 0:
        return False

    return True


def isCityNameDuplicated(name: str, code: str) -> bool:
    '''
        Calls persistance layer to see if a city has the same name.
    '''

    call = dm.get_by_property("cities", "country_code", code)

    for city in call:
        if city["name"] == name:
            return True

    return False


def isOwnerIDTheSame(place_id: str, user_id: str) -> bool:
    '''
        Calls persistance layer to compare the owner id of a place with the
        given id.
    '''

    call = dm.get(place_id)

    return call["host_id"] == user_id


def doesCountryExist(country_code: str) -> bool:
    '''
        Checks if a country exists.
    '''

    for country in getCountries():
        if country["code"] == country_code:
            return True

    return False
