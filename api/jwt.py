
'''
    Defines how to authorize endpoints using JWT.
'''

from flask_jwt_extended import JWTManager


def createJWT() -> JWTManager:
    '''
        Makes and returns a JWTManager.

        Used for the factory pattern.
    '''

    jwt = JWTManager()

    return jwt
