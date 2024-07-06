
'''
    Provides common functions for testing.
'''

import inspect
from io import TextIOWrapper
from typing import Any
import requests
import json
from pathlib import Path
import time

import requests.structures

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
RESET = "\033[0m"


class AuthFailure(Exception):
    '''Failure to authenticate as admin'''


class HTTPTestClass:
    '''
        Test Base Class for testing the API.
        Test Classes inherit from this class to get all methods.
        Flask Server must be running for tests to work.
        If debug == True it shows the result of all passed assertions.
    '''

    local_url: str = "http://127.0.0.1:5000/"
    _root_path = Path(__file__).parent.parent.resolve()

    assertions_passed: int = 0
    assertions_failed: int = 0
    tests_passed: int = 0
    tests_failed: int = 0
    num_http: int = 0
    last_response: requests.Response | None = None
    last_post_id: str | None = None
    last_failed: bool = False
    json: dict = {}
    headers: dict = {'Content-type': 'application/json',
                     'Accept': 'application/json'}
    token: str | None = None
    prefix: str = f">>> "
    suffix: str = f"{RESET}"
    debug: bool = False

    @classmethod
    def _ASSERTION_SUCCESS(
        cls,
        msg: str | None = None
    ) -> None:

        if msg is None:
            msg = "Assertion Passed"
        if cls.debug:
            print(f"{cls.prefix}{GREEN}{msg}{cls.suffix}")
        cls.assertions_passed += 1

    @classmethod
    def _ASSERTION_FAILURE(
        cls,
        errormsg: str | None = None
    ) -> None:

        if errormsg is None:
            errormsg = "Assertion Failed"
        cls.assertions_failed += 1
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

        code = cls.last_response.status_code
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

        data = cls.last_response.json()
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
        if url == "flask":
            cls.local_url = "http://127.0.0.1:5000/"
        elif url == "gunicorn":
            cls.local_url = "http://127.0.0.1:8000/"
        else:
            cls.local_url = url

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
    def CLEAN(cls) -> None:
        cls.json = {}
        cls.last_response = None
        cls.headers = {'Content-type': 'application/json',
                       'Accept': 'application/json'}

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
        return cls.last_response.status_code

    @classmethod
    def GET_RESPONSE_HEADERS(cls) -> dict:
        return dict(cls.last_response.headers)

    @classmethod
    def GET_RESPONSE_JSON(cls) -> dict:
        return cls.last_response.json()

    @classmethod
    def GET_RESPONSE_TEXT(cls) -> dict:
        return cls.last_response.text

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
    def SAVE_RESPONSE(cls, filename: str = "log.txt"):
        '''
            Save response to file.
        '''

        def writeHell(
                obj: object,
                file: TextIOWrapper,
                level: int = 0
        ) -> None:
            '''
                Writes in a beautiful way.
            '''

            def goodWrite(string: str):
                str_len = len(string)
                l = 0
                if str_len < 80:
                    file.write(string)
                    return
                for i in range(str_len // 80):
                    file.write(string[i * 80: (i + 1) * 80])
                    file.write("\n")
                    l = i
                file.write(string[(l + 1) * 80:])

            if isinstance(obj, dict):
                len_of_obj = len(obj) - 1
                f.write("{")
                for i, key in enumerate(obj):
                    file.write(f"{key}: ")
                    if (isinstance(obj[key], dict) or
                            isinstance(obj[key], list)):
                        writeHell(obj[key], file, level + 1)
                    else:
                        goodWrite(f"{repr(key)}: {repr(obj[key])}")
                    if len_of_obj != i:
                        f.write(", ")
                    if i % 3 == 2:
                        f.write("\n")
                f.write("}")
            elif isinstance(obj, list):
                len_of_obj = len(obj) - 1
                f.write("[")
                for i, element in enumerate(obj):
                    writeHell(element, file, level + 1)
                    if len_of_obj != i:
                        f.write(", \n")
                f.write("]")
            else:
                f.write("  " * level)
                goodWrite(f"- {str(obj)}")

        with open(filename, "a+") as f:
            response = cls.GET_RESPONSE()
            f.write("\n---\n")
            f.write("\ncode:\n")
            writeHell(response["code"], f)
            f.write("\nheaders:\n")
            writeHell(response["headers"], f)
            f.write("\njson:\n")
            writeHell(response["json"], f)
            f.write("\ntext:\n")
            writeHell(response["text"], f)
            f.write("\n---\n")

    @classmethod
    def GET_RESPONSE_VALUE(cls, key: str):
        return cls.last_response.json()[key]

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

        data = cls.last_response.json()
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
        if cls.last_response.status_code != 200:
            cls.assertions_failed += 1
            cls.tests_failed += 1
            raise AuthFailure()
        token = cls.last_response.json["access_token"]
        cls.token = token
        cls.headers.update({"Authorization": f"Bearer {token}"})
        cls.last_failed = False
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
        if cls.last_response.status_code != 200:
            cls.assertions_failed += 1
            cls.tests_failed += 1
            raise AuthFailure()
        token = cls.last_response.json()["access_token"]
        cls.token = token
        cls.headers.update({"Authorization": f"Bearer {token}"})
        cls.last_failed = False
        return token

    @classmethod
    def GET(cls, endpoint: str) -> int:
        '''
            HTTP GET request.
        '''

        response = requests.get(
            f"{cls.local_url}{endpoint}", headers=cls.headers)
        cls.last_response = response
        cls.num_http += 1
        cls.last_failed = False
        return response.status_code

    @classmethod
    def POST(cls, endpoint: str) -> int:
        '''
            HTTP POST request.
        '''

        response = requests.post(
            f"{cls.local_url}{endpoint}",
            json=cls.json,
            headers=cls.headers
        )
        cls.last_response = response
        try:
            cls.last_post_id = response.json().get("id")
        except Exception:
            pass
        cls.num_http += 1
        cls.last_failed = False
        return response.status_code

    @classmethod
    def PUT(cls, endpoint: str) -> int:
        '''
            HTTP PUT request.
        '''

        response = requests.put(
            f"{cls.local_url}{endpoint}",
            json=cls.json,
            headers=cls.headers
        )
        cls.last_response = response
        cls.num_http += 1
        cls.last_failed = False
        return response.status_code

    @classmethod
    def DELETE(cls, endpoint: str) -> int:
        '''
            HTTP DELETE request.
        '''

        response = requests.delete(
            f"{cls.local_url}{endpoint}", headers=cls.headers)
        cls.last_response = response
        cls.num_http += 1
        cls.last_failed = False
        return response.status_code

    @classmethod
    def Setup(cls) -> None:
        '''
            Called before each test. Can be ovewritten.
        '''

        cls.last_post_id = None

    @classmethod
    def Teardown(cls) -> None:
        '''
            Called after the ending of each test. Made to be overwritten.
        '''

        pass

    @classmethod
    def run(cls, *, url=None, only_output_errors=False) -> tuple[int, int]:
        '''
            Gets all methods, and then filters them to get only methods that
            have the word "test" in them and are not from Object.
        '''

        if url is not None:
            cls.CHANGE_URL = url

        methods = inspect.getmembers(cls, lambda a: inspect.isroutine(a))
        tests = {
                 attr: func for attr, func in methods if
                 not (attr[0:2] == "__" and attr[-2:] == "__") and
                 attr.find("test") != -1
                }

        if not only_output_errors:
            print(f"{cls.prefix}{MAGENTA}",
                  f"Running {cls.__name__}...",
                  f"{cls.suffix}")
        for name in tests:
            time.sleep(0.1)
            if not only_output_errors:
                print(f"{cls.prefix}{YELLOW}" +
                      f"Running {name}..." +
                      f"{cls.suffix}")
            try:
                cls.Setup()
                tests[name]()
                cls.tests_passed += 1
            except AssertionError as err:
                print(f"{cls.prefix}{RED}Check failed on {name}:{RESET}\n" +
                      f"{err}{cls.suffix}\n")
                if cls.last_response is not None:
                    print(f"\t[{cls.last_response.request.method}]")
                    print(f"\t-{cls.last_response.request.url}")
                    print(f"\t-{cls.last_response.reason}")
                    print(f"\n\t{RED}RESPONSE:{RESET}")
                    print(f"{cls.last_response.text}")
                    print(f"\n\t{RED}JSON:{RESET}")
                    print(f"{cls.json}\n")
                cls.last_failed = True
                cls.tests_failed += 1
            except KeyError as err:
                print(f"{cls.prefix}{RED}{name}did not find key to check:" +
                      f"{RESET}\n\t{err}{cls.suffix}")
                cls.last_failed = True
                cls.tests_failed += 1
            except AuthFailure as err:
                print(f"{cls.prefix}{RED}{cls.__name__}: " +
                      f"Could not authenticate as admin{cls.suffix}")
                tests = {}
                break
            finally:
                cls.Teardown()

        if cls.tests_failed == 0:
            print(f"{cls.prefix}{GREEN}All tests from " +
                  f"{cls.__name__} passed: ", end="")
        elif cls.tests_passed == 0:
            print(f"{cls.prefix}{RED}All tests from " +
                  f"{cls.__name__} failed: ", end="")
        else:
            print(f"{cls.prefix}{YELLOW}Some tests from " +
                  f"{cls.__name__} failed: ", end="")
        tests_total = cls.tests_passed + cls.tests_failed
        assertions_total = cls.assertions_failed + cls.assertions_passed
        print(f"{RESET}{cls.tests_passed}/{tests_total} Tests, " +
              f"{cls.assertions_passed}/{assertions_total} Assertions, " +
              f"{cls.num_http} HTTP Requests." +
              f"{cls.suffix}\n")
        return cls.tests_failed, cls.tests_passed, cls.num_http
