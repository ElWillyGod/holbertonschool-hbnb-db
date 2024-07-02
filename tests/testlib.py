
'''
    Provides common functions for testing.
'''

import inspect
from typing import Any
import requests
import json
from pathlib import Path
import time

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
RESET = "\033[0m"


class HTTPTestClass:
    '''
        Test Base Class for testing the API.
        Test Classes inherit from this class to get all methods.
        Flask Server must be running for tests to work.
        If debug == True it shows the result of all passed assertions.
    '''

    local_URL: str = "http://127.0.0.1:5000/"
    _root_path = Path(__file__).parent.parent.resolve()

    assertionsPassed: int = 0
    assertionsFailed: int = 0
    testsPassed: int = 0
    testsFailed: int = 0
    num_http: int = 0
    lastResponse: requests.Response | None = None
    json: dict = {}
    headers: dict = {'Content-type': 'application/json',
                     'Accept': 'application/json'}
    token: str | None = None
    prefix: str = f">>> "
    suffix: str = f"{RESET}"
    debug: bool = False

    @classmethod
    def _ASSERTION_SUCCESS(cls,
                           msg: str | None = None
                           ) -> None:

        if msg is None:
            msg = "Assertion Passed"
        if cls.debug:
            print(f"{cls.prefix}{GREEN}{msg}{cls.suffix}")
        cls.assertionsPassed += 1

    @classmethod
    def _ASSERTION_FAILURE(
        cls,
        errormsg: str | None = None
) -> None:

        if errormsg is None:
            errormsg = "Assertion Failed"
        cls.assertionsFailed += 1
        raise AssertionError(errormsg)

    @classmethod
    def _ASSERT(
        cls,
        value: Any,
        expected_value: Any,
        errormsg: str | None = None
) -> None:
        msg = f"\tExpected: {expected_value}\n\tGiven: {value}"
        errormsg = msg if errormsg is None else errormsg
        if value == expected_value:
            cls._ASSERTION_SUCCESS(errormsg)
        else:
            cls._ASSERTION_FAILURE(errormsg)

    @classmethod
    def ASSERT_CODE(
        cls,
        code_expected: int,
        errormsg: str | None = None
) -> None:
        '''
            Asserts that the code of last response is equal to the
            code expected.
        '''

        code = cls.lastResponse.status_code
        cls._ASSERT(code, code_expected, errormsg)

    @classmethod
    def ASSERT_VALUE(
        cls,
        key: str,
        value_expected: Any,
        errormsg: str | None = None
) -> None:
        '''
            Asserts that the value of key of last response is equal to the
            value expected.
        '''

        data = cls.lastResponse.json()
        if isinstance(data, list):
            found_one = False
            for dic in data:
                if key in dic:
                    value = dic[key]
                    found_one = True
                    if value == value_expected:
                        cls._ASSERT(value, value_expected, errormsg)
                        return
            if found_one:
                if errormsg is None:
                    errormsg = (f"No key with expected value found " +
                    f"{key}: {value_expected}")
                raise AssertionError(errormsg)
            else:
                raise KeyError(f"key not found for test: {key}")

        if key not in data:
            raise KeyError(f"key not found for test: {key}")
        value = data[key]
        cls._ASSERT(value, value_expected, errormsg)

    @classmethod
    def CHANGE_URL(cls, url: str) -> None:
        cls.local_URL = url

    @classmethod
    def CHANGE_URL_TO_FLASK(cls) -> None:
        cls.local_URL = "http://127.0.0.1:5000/"

    @classmethod
    def CHANGE_URL_TO_GUNICORN(cls) -> None:
        cls.local_URL = "http://127.0.0.1:8000/"

    @classmethod
    def FROM(cls, filename: str) -> None:
        '''
            Store into a dictionary all the data of a json file.
            Subsequent POST and PUT will use this data.
        '''

        current_dir = Path(__file__).parent.resolve()
        content: dict
        with open(f"{current_dir}/{filename}", "r") as file:
            content = json.load(file)
        cls.json = content

    @classmethod
    def GET_JSON(cls):
        return cls.json

    @classmethod
    def GET_HEADERS(cls):
        return cls.headers

    @classmethod
    def GET_TOKEN(cls):
        return cls.token

    @classmethod
    def CLEAR(cls) -> None:
        cls.json = {}
        cls.lastResponse = None

    @classmethod
    def SET_VALUE(cls, key: str, value: Any):
        '''
            Set data of key to value from stored data.
        '''

        cls.json[key] = value

    @classmethod
    def GET_VALUE(cls, key: str) -> None:
        '''
            Gets value from key from stored data.
        '''

        return cls.json[key]

    @classmethod
    def REMOVE_VALUE(cls, key: str) -> None:
        '''
            Removes value from stored data.
        '''

        cls.json.pop(key)

    @classmethod
    def GET_RESPONSE_CODE(cls) -> int:
        return cls.lastResponse.status_code

    @classmethod
    def GET_RESPONSE_HEADERS(cls) -> dict:
        return cls.lastResponse.headers

    @classmethod
    def GET_RESPONSE_JSON(cls) -> dict:
        return cls.lastResponse.json()

    @classmethod
    def GET_RESPONSE_TEXT(cls) -> dict:
        return cls.lastResponse.text

    @classmethod
    def GET_RESPONSE(cls) -> dict:
        '''
            Combines all the gets from response.
        '''

        try:
            code = cls.GET_RESPONSE_CODE()
        except Exception:
            code = ""
        try:
            headers = cls.GET_RESPONSE_HEADERS()
        except Exception:
            headers = ""
        try:
            text = cls.GET_RESPONSE_TEXT()
        except Exception:
            text = ""
        try:
            json = cls.GET_RESPONSE_JSON()
        except Exception:
            json = ""

        return {"code": code, "headers": headers, "json": json, "text": text}

    @classmethod
    def GET_RESPONSE_VALUE(cls, key: str):
        return cls.lastResponse.json()[key]

    @classmethod
    def GET_RESPONSE_WITH(
        cls,
        key: str,
        value: str,
        key_target: str
) -> Any:
        '''
            Gets value from key_target from object with
            key and value of last response.
        '''

        data = cls.lastResponse.json()
        if isinstance(data, dict):
            if key not in data:
                raise KeyError(f"object does not present {key}")
            if data[key] != value:
                raise AssertionError(f"object's value does not match")
            if key_target not in data:
                raise KeyError(f"object does not have '{key_target}'")
            return data[key_target]
        else:
            for dic in data:
                if key not in dic:
                    continue
                if dic[key] != value:
                    continue
                if key_target not in dic:
                    raise KeyError(f"object does not have '{key_target}'")
                return dic[key_target]
            raise KeyError(f"object not found: {key}")

    @classmethod
    def AUTH(cls, email: str, password: str) -> str:
        '''
            Authenticate from an email and a password.
        '''

        cls.json = {"email": email, "password": password}
        cls.POST("/login")
        cls.ASSERT_CODE(200)
        token = cls.lastResponse.json["access_token"]
        cls.token = token
        cls.headers.update({"Authorization": f"Bearer {token}"})
        return token

    @classmethod
    def AUTH_FROM(cls, filename: str) -> str:
        '''
            Authenticate from a user in a json file.
        '''

        user: dict
        with open(filename, "r") as f:
            user = json.load(f)
        email = user["email"]
        password = user["password"]
        cls.json = {"email": email, "password": password}
        cls.POST("/login")
        cls.ASSERT_CODE(200)
        token = cls.lastResponse.json()["access_token"]
        cls.token = token
        cls.headers.update({"Authorization": f"Bearer {token}"})
        return token

    @classmethod
    def GET(cls, endpoint: str) -> int:
        '''
            HTTP GET request.
        '''

        response = requests.get(
            f"{cls.local_URL}{endpoint}", headers=cls.headers)
        cls.lastResponse = response
        cls.num_http += 1
        return response.status_code

    @classmethod
    def POST(cls, endpoint: str) -> int:
        '''
            HTTP POST request.
        '''

        response = requests.post(
            f"{cls.local_URL}{endpoint}",
            json=cls.json,
            headers=cls.headers
        )
        cls.lastResponse = response
        cls.num_http += 1
        return response.status_code

    @classmethod
    def PUT(cls, endpoint: str) -> int:
        '''
            HTTP PUT request.
        '''

        response = requests.put(
            f"{cls.local_URL}{endpoint}",
            json=cls.json,
            headers=cls.headers
        )
        cls.lastResponse = response
        cls.num_http += 1
        return response.status_code

    @classmethod
    def DELETE(cls, endpoint: str) -> int:
        '''
            HTTP DELETE request.
        '''

        response = requests.delete(
            f"{cls.local_URL}{endpoint}", headers=cls.headers)
        cls.lastResponse = response
        cls.num_http += 1
        return response.status_code

    @classmethod
    def Teardown(cls) -> None:
        '''
            Called after the ending of each test. Made to be overriden.
        '''

        pass

    @classmethod
    def run(cls) -> tuple[int, int]:
        '''
            Gets all methods, and then filters them to get only methods that
            have the word "test" in them and are not from Object.
        '''

        methods = inspect.getmembers(cls, lambda a: inspect.isroutine(a))
        tests = {
                 attr: func for attr, func in methods if
                 not (attr[0:2] == "__" and attr[-2:] == "__") and
                 attr.find("test") != -1
                }

        print(f"{cls.prefix}{MAGENTA}Running {cls.__name__}...{cls.suffix}")
        for name in tests:
            time.sleep(0.1)
            print(f"{cls.prefix}{YELLOW}Running {name}...{cls.suffix}")
            try:
                tests[name]()
                cls.testsPassed += 1
            except AssertionError as e:
                print(f"{cls.prefix}{RED}Check failed on {name}:{RESET}\n" +
                      f"{e}{cls.suffix}\n")
                print(f"\t[{cls.lastResponse.request.method}]")
                print(f"\t-{cls.lastResponse.request.url}")
                print(f"\t-{cls.lastResponse.reason}")
                print(f"\n\t{RED}RESPONSE:{RESET}")
                print(f"{cls.lastResponse.text}")
                print(f"\n\t{RED}JSON:{RESET}")
                print(f"{cls.json}\n")
                cls.testsFailed += 1
            except KeyError as e:
                print(f"{cls.prefix}{RED}{name} did not find key to check:" +
                      f"{RESET}\n\t{e}{cls.suffix}")
                cls.testsFailed += 1
            finally:
                cls.Teardown()

        if cls.testsFailed == 0:
            print(f"{cls.prefix}{GREEN}All tests from " +
                  f"{cls.__name__} passed: ", end="")
        elif cls.testsPassed == 0:
            print(f"{cls.prefix}{RED}All tests from " +
                  f"{cls.__name__} failed: ", end="")
        else:
            print(f"{cls.prefix}{YELLOW}Some tests from " +
                  f"{cls.__name__} failed: ", end="")
        tests_total = cls.testsPassed + cls.testsFailed
        assertions_total = cls.assertionsFailed + cls.assertionsPassed
        print(f"{RESET}{cls.testsPassed}/{tests_total} Tests, " +
              f"{cls.assertionsPassed}/{assertions_total} Assertions, " +
              f"{cls.num_http} HTTP Requests." +
              f"{cls.suffix}\n")
        return cls.testsFailed, cls.testsPassed
