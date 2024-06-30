
'''
    Defines LogicFacade and calls integration layer to get countries.
    This static class is called from API to handle HTTP requests logically.
    Imports from integration layer are WIP.
'''

from abc import ABC

from logic.model.classes import getClassByName
from logic.model.countrieslib import getCountry, getCountries
from logic.model.logicexceptions import IDNotFoundError
from logic.model.validationlib import idExists
from logic import DM as Persistence
from logic.model.linkeddeleter import raiseDeleteEvent
from api import app
from logic.model import amenity


class LogicFacade(ABC):
    '''
        Static class that defines static methods meant to be called from API.

        Each method handles a particular HTTP request.
        The get methods return dictionaries.
        Data arguments should also be dictionaries.

        --HTTP--
        GET:
            getByType(cls: str) -> dict
            getByID(id: str, cls: str) -> dict
            getCountry(code: str) -> dict
            getAllCountries() -> dict
            getCountryCities(code: str) -> dict
            getReviewsOfPlace(id: str) -> dict
        POST:
            createObjetByJson(cls: str, data: dict) -> None
        PUT:
            updateByID(id: str, cls: str, data: dict) -> None
        DELETE:
            deleteByID(id: str, cls: str) -> Node
    '''

    @staticmethod
    def getByType(type: str) -> dict:
        return Persistence.get_all(type)

    @staticmethod
    def getByID(id: str, type: str) -> dict:
        call = Persistence.get(id, type)
        if call is None or len(call) == 0:
            raise IDNotFoundError("id not found")
        return call

    @staticmethod
    def deleteByID(id: str, type: str) -> None:
        call = Persistence.get(id, type)
        if call is None or len(call) == 0:
            raise IDNotFoundError("id not found")
        raiseDeleteEvent(type, call)
        Persistence.delete(id, type)

    @staticmethod
    def updateByID(id: str, type: str, data: dict) -> dict:
        old_data = Persistence.get(id, type)
        if old_data is None or len(old_data) == 0:
            raise IDNotFoundError("id not found")
        updated = []
        for key in data:
            if data[key] != old_data[key]:
                updated.append(key)
        data["id"] = id
        data["created_at"] = old_data["created_at"]
        data["updated_at"] = None
        data_updated = getClassByName(type)(**data, update=updated)
        Persistence.update(id, type, data_updated.toJson())
        return Persistence.get(id, type)

    @staticmethod
    def createObjectByJson(type: str, data: dict) -> dict:
        new = getClassByName(type)(**data)
        print("esto es el new {}".format(new))
        return Persistence.save(new.id, type, new if app.config['USE_DATABASE'] else new.toJson())
        # return Persistence.get(id, typePlural)

    @staticmethod
    def getAllCountries() -> dict:
        return getCountries()

    @staticmethod
    def getCountry(code: str) -> dict:
        return getCountry(code)

    @staticmethod
    def getContryCities(code: str) -> dict:
        return Persistence.get_by_property(
            "cities", "country_code", code
        )

    @staticmethod
    def getReviewsOfPlace(id: str) -> dict:
        if not idExists(id, 'places'):
            raise IDNotFoundError("id not found")
        return Persistence.get_by_property(
            "places", "id", id
        )
