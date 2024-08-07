
'''
    Defines validation functions.
    Makes calls to the persistance layer.
'''

from logic.model.amenity import Amenity
from logic.model.city import City
from logic.model.review import Review
from logic.model.user import User
from logic.model.country import Country
from logic.model.place import Place
from persistence import dm
from logic.model.countrieslib import getCountries
from logic.model.logicexceptions import *


def validationManager(obj):
    '''
        Validates stuff
    '''

    if obj.__class__ == Amenity:
        isAmenityDuplicated(obj)

    if obj.__class__ == User:
        isUserEmailDuplicated(obj)

    if obj.__class__ == City:
        doesCountryExist(obj)
        isCityNameDuplicated(obj)

    if obj.__class__ == Country:
        doesCountryExist(obj)

    if obj.__class__ == Review:
        if not (idExists(Place(id=obj.place_id))):
            raise IDNotFoundError("place_id doesn't pair with a place")

        if not (idExists(User(id=obj.user_id))):
            raise IDNotFoundError("user_id doesn't pair with a user")

        if isOwnerIDTheSame(Place(id=obj.place_id), User(id=obj.user_id)):
            raise TryingToReviewOwnPlace("you cannot review your own place")

    if obj.__class__ == Place:

        if not idExists(User(id=obj.host_id)):
            raise IDNotFoundError("host_id does not exist")
        if not idExists(City(id=obj.city_id)):
            raise IDNotFoundError("city_id does not exist")
        for amenity in obj.amenity_ids:
            if not idExists(amenity):
                raise IDNotFoundError(
                    f"'{amenity.id}' in amenity_ids does not exist")


def idExists(obj) -> bool:
    '''
        Calls persistance layer to see if an id of type cls exists.
    '''

    call = dm.read(obj)

    if call is None or len(call) == 0:
        return False

    return True

def isUserEmailDuplicated(user):
    '''
        Calls persistance layer to see if a user has the same email.
    '''

    call = dm.get_by_property(user.__class__, "email", user.email)

    if not (call is None or len(call) == 0):
        raise EmailDuplicated("email already exists")



def isAmenityDuplicated(amenity):
    '''
        Calls persistance layer to see if a user has the same email.
    '''

    call = dm.get_by_property(amenity.__class__, "name", amenity.name)

    if not (call is None or len(call) == 0):
        raise AmenityNameDuplicated("amenity already exists")


def isCityNameDuplicated(city):
    '''
        Calls persistance layer to see if a city has the same name.
    '''

    call = dm.get_by_property(city, "country_code", city.country_code)

    for city in call:
        if city.name == city.name:
                raise CityNameDuplicated(
                    f"{city.name} already exists in {city.country_code}")


def isOwnerIDTheSame(place, user) -> bool:
    '''
        Calls persistance layer to compare the owner id of a place with the
        given id.
    '''

    place = dm.read(place)

    return place.host_id == user.id


def doesCountryExist(obj):
    '''
        Checks if a country exists.
    '''

    for country in getCountries():
        if country["code"] == obj.country_code:
            return

    raise CountryNotFoundError(
            f"country '{obj.country_code}' not found")
