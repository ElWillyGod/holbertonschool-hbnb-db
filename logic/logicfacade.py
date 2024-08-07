
'''
    Defines LogicFacade and calls integration layer to get countries.
    This static class is called from API to handle HTTP requests logically.
    Imports from integration layer are WIP.
'''

from abc import ABC

from logic.model import classes
from logic.model.countrieslib import getCountry, getCountries
from logic.model.logicexceptions import IDNotFoundError, EmailNotFoundError
from logic.model.validationlib import idExists, validationManager
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
        all = Persistence.get_all(obj)
        return [obj.toJson() for obj in all]

    @staticmethod
    def getByID(
        id: str,
        type: str
) -> dict:
        obj = classes.getObjectByName(type)
        call = Persistence.read(obj(id=id))
        if call is None:
            raise IDNotFoundError("id not found")
        return call.toJson()

    @staticmethod
    def deleteByID(
        id: str,
        type: str,
        email: str = "",
        is_admin: bool = False
) -> None:
        obj = classes.getObjectByName(type)
        obj.checkThatItCanBeModifiedBy(id, email, is_admin)
        Persistence.delete(obj(id=id))

    @staticmethod
    def updateByID(
        id: str,
        type: str,
        data: dict,
        email: str = "",
        is_admin: bool = False
) -> dict:
        obj = classes.getObjectByName(type)
        obj.checkThatItCanBeModifiedBy(id, email, is_admin)
        obj = obj(id=id, **data)
        if not (idExists(obj)):
            raise IDNotFoundError("id not found")
        validationManager(obj)
        Persistence.update(obj, is_admin)
        return Persistence.read(obj).toJson()

    @staticmethod
    def createObjectByJson(
        type: str,
        data: dict,
        email: str = "",
        is_admin: bool = False
) -> dict:
        obj = classes.getObjectByName(type)
        obj.checkThatItCanBeCreatedBy(data, email, is_admin)
        obj = obj(**data)
        validationManager(obj)
        Persistence.create(obj, is_admin)
        return Persistence.read(obj).toJson()

    @staticmethod
    def getAllCountries() -> dict:
        return getCountries()

    @staticmethod
    def getCountry(code: str) -> dict:
        return getCountry(code)

    @staticmethod
    def getContryCities(code: str) -> dict:
        return Persistence.get_by_property(
            classes.City, "country_code", code
        ).toJson()

    @staticmethod
    def getReviewsOfPlace(id: str) -> dict:
        if not idExists(classes.Place(id=id)):
            raise IDNotFoundError("id not found")
        return Persistence.get_by_property(
            classes.Review, "id", id
        )

    @staticmethod
    def getPswdAndAdminByEmail(
        email: str
) -> tuple[str, bool]:
        user = Persistence.get_by_property(classes.User, "email", email)
        if not user:
            raise EmailNotFoundError("email not found")
        # user is transformed from list to dict
        user = user[0]
        return user.password, user.is_admin
