
'''
    Defines all variables for app.config
'''

from os import environ

SQLITE_DB = environ.get("SQLITE_DB")
if SQLITE_DB:
    sqlite_uri = f"sqlite:///{SQLITE_DB}"
else:
    sqlite_uri = None

MYSQL_DRIVER = environ.get("MYSQL_DRIVER")
MYSQL_HOST = environ.get("MYSQL_HOST")
if MYSQL_DRIVER and MYSQL_HOST:
    mysql_uri = f"mysql+{MYSQL_DRIVER}://user:password@{MYSQL_HOST}/hbnb"
else:
    mysql_uri = None

MYSQL_ACCESS_LEVEL_1 = environ.get("MYSQL_ACCESS_LEVEL_1")
MYSQL_ACCESS_LEVEL_2 = environ.get("MYSQL_ACCESS_LEVEL_2")
MYSQL_ACCESS_LEVEL_3 = environ.get("MYSQL_ACCESS_LEVEL_3")
MYSQL_ACCESS_LEVEL_ROOT = environ.get("MYSQL_ACCESS_LEVEL_ROOT")


class Config:
    '''
        Base class for configuration classes.
        Defines URI definition.
    '''

    SECRET_KEY = environ.get("SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY is required.")

    DATABASE_TYPE = environ.get("DATABASE_TYPE", "sqlite")

    if DATABASE_TYPE == "sqlite":
        if sqlite_uri:
            SQLALCHEMY_DATABASE_URI = mysql_uri
        else:
            raise ValueError("Trying to use sqlite without database filename")
    else:
        if MYSQL_ACCESS_LEVEL_ROOT:
            SQLALCHEMY_DATABASE_URI = mysql_uri.\
                replace("user", "root").\
                replace("password", MYSQL_ACCESS_LEVEL_ROOT)
        else:
            if not (MYSQL_ACCESS_LEVEL_1 and
                    MYSQL_ACCESS_LEVEL_2 and
                    MYSQL_ACCESS_LEVEL_3):
                raise ValueError(
                    "Trying to use access levels without setting them")
            SQLALCHEMY_DATABASE_URI = mysql_uri.\
                replace("user", "access_level_3").\
                replace("password", MYSQL_ACCESS_LEVEL_3)
            SQLALCHEMY_BINDS = {
                "access_level_2": mysql_uri.\
                    replace("user", "access_level_2").\
                    replace("password", MYSQL_ACCESS_LEVEL_2),
                "access_level_3": mysql_uri.\
                    replace("user", "access_level_1").\
                    replace("password", MYSQL_ACCESS_LEVEL_1)
            }

class ProductionConfig(Config):
    '''
        Configuration settings for prodution.
        In production some values if not configured will raise an error.
    '''

    if Config.DATABASE_TYPE is None or Config.DATABASE_TYPE != "mysql":
        raise ValueError("DATABASE_TYPE must be mysql for production")

    if not mysql_uri:
        raise ValueError("MySQL config required for production setting")

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

class TestingConfig(Config):
    '''
        Configuration settings for prodution.
    '''

    SQLALCHEMY_ECHO = environ.get(
        "SQLALCHEMY_ECHO",
        default=True
    )

    SQLALCHEMY_RECORD_QUERIES = environ.get(
        "SQLALCHEMY_RECORD_QUERIES",
        default=True
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = environ.get(
        "SQLALCHEMY_TRACK_MODIFICATIONS",
        default=False
    )

    SQLALCHEMY_COMMIT_ON_TEARDOWN = environ.get(
        "SQLALCHEMY_COMMIT_ON_TEARDOWN",
        default=False
    )

class DevelopmentConfig(Config):
    '''
        Configuration settings for prodution.
    '''

    SQLALCHEMY_ECHO = environ.get(
        "SQLALCHEMY_ECHO",
        default=True
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
