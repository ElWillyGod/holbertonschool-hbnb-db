
'''
    Defines all variables for app.config
'''

from os import environ

SECRET_KEY = environ.get("SECRET_KEY", default="SomethingWentWrong")

DATABASE_TYPE = environ.get(
    "DATABASE_TYPE",
    default="sqlite"
)

SQLALCHEMY_DATABASE_URI = environ.get(
    "DATABASE_URL",
    default="sqlite:///dev.db"
)

SQLALCHEMY_ECHO = environ.get(
    "SQLALCHEMY_ECHO",
    default=False
)

SQLALCHEMY_RECORD_QUERIES = environ.get(
    "SQLALCHEMY_RECORD_QUERIES",
    default=False
)

SQLALCHEMY_TRACK_MODIFICATIONS = environ.get(
    "SQLALCHEMY_TRACK_MODIFICATIONS",
    default=False
)

SQLALCHEMY_COMMIT_ON_TEARDOWN = environ.get(
    "SQLALCHEMY_COMMIT_ON_TEARDOWN",
    default=False
)
