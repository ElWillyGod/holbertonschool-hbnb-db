
'''
    Defines functions that checks if the user is forbidden of doing a request.

    All of these functions return None if authorized, and an error message if
    not.

    They are called on all requests, so authorizations are in one single file
    and can be modified without going to the endpoints.

    Authorization that depends of the user id is done in model.
'''

ERROR_MSG = "Requires admin privileges"


def _isAdmin(user: dict | None) -> bool:
    '''
        Returns true if user is an admin (is_admin == True).
    '''

    return user.get("is_admin", False)


def notGetAllAuthorized(
    tipo: str,
    user: dict | None
) -> None | str:
    '''
        Manages get all request authorization.
    '''

    if tipo == "user":
        if not _isAdmin(user):
            return ERROR_MSG

    return None


def notGetAuthorized(
    tipo: str,
    user: dict | None
) -> None | str:
    '''
        Manages get request authorization.
    '''

    return None


def notPostAuthorized(
    tipo: str,
    user: dict | None
) -> None | str:
    '''
        Manages post request authorization.
    '''

    if tipo == "user":
        if not _isAdmin(user):
            return ERROR_MSG

    if tipo == "city":
        if not _isAdmin(user):
            return ERROR_MSG

    if tipo == "amenity":
        if not _isAdmin(user):
            return ERROR_MSG

    return None


def notPutAuthorized(
    tipo: str,
    user: dict | None
) -> None | str:
    '''
        Manages put request authorization.
    '''

    if tipo == "user":
        if not _isAdmin(user):
            return ERROR_MSG

    if tipo == "city":
        if not _isAdmin(user):
            return ERROR_MSG

    if tipo == "amenity":
        if not _isAdmin(user):
            return ERROR_MSG

    return None


def notDeleteAuthorized(
    tipo: str,
    user: dict | None
) -> None | str:
    '''
        Manages delete request authorization.
    '''

    if tipo == "user":
        if not _isAdmin(user):
            return ERROR_MSG

    if tipo == "city":
        if not _isAdmin(user):
            return ERROR_MSG

    if tipo == "amenity":
        if not _isAdmin(user):
            return ERROR_MSG

    return None
