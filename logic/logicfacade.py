
'''
    Defines LogicFacade and calls integration layer to get countries.
    This static class is called from API to handle HTTP requests logically.
    Imports from integration layer are WIP.
'''

from abc import ABC

from logic.model import classes
from logic.model.classes import getObjectByName
from logic.model.countrieslib import getCountry, getCountries
from logic.model.logicexceptions import IDNotFoundError, EmailNotFoundError
from logic.model.validationlib import idExists
from persistence import dm as Persistence


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
        obj = classes.getObjectByName(type)
        return Persistence.get_all(obj)

    @staticmethod
    def getByID(
        id: str,
        type: str
) -> dict:
        obj = classes.getObjectByName(type)
        call = Persistence.read(id, obj)
        if call is None or len(call) == 0:
            raise IDNotFoundError("id not found")
        return call.toJson()

    @staticmethod
    def deleteByID(
        id: str,
        type: str
) -> None:
        obj = classes.getObjectByName(type)
        call = Persistence.read(id, obj)
        if call is None or len(call) == 0:
            raise IDNotFoundError("id not found")
        Persistence.delete(id, obj)

    @staticmethod
    def updateByID(
        id: str,
        type: str,
        data: dict
) -> dict:
        obj = classes.getObjectByName(type)
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
        data_updated = getObjectByName(type)(**data, update=updated)
        Persistence.update(id, type, data_updated.toJson())
        return Persistence.read(id, type).toJson()

    @staticmethod
    def createObjectByJson(
        type: str,
        data: dict
) -> dict:
        obj = classes.getObjectByName(type)
        new = obj(**data)
        id = new.id
        return Persistence.create(id, type, new).toJson()
        # return Persistence.get(id, type)

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

    @staticmethod
    def getPswdAndAdminByEmail(
        email: str
) -> tuple[str, bool]:
        user = Persistence.get_by_property("users", "email", email)
        if not user:
            raise EmailNotFoundError("email not found")
        # user is transformed from list to dict
        user = user[0]
        return user["password"], user["id"], user["is_admin"]
