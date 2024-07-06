#!/usr/bin/python3

'''
    Defines smoke test class.

    Tests if nothing awful occurs on execution to save time.
'''
import sys
from testlib import HTTPTestClass
from requests.exceptions import ConnectionError

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
WHITE = "\033[37m"
RESET = "\033[0m"


class SmokeFailure(Exception):
    '''Called when smoke test fails'''


class TestSmoke(HTTPTestClass):
    '''
        Defines smoke test (test if server is up)
    '''

    @classmethod
    def Teardown(cls) -> None:
        if cls.tests_failed >= 1:
            raise AssertionError()

    @classmethod
    def test_00_smoke_api(cls):
        try:
            cls.GET("/apidocs")
            if cls.last_response.status_code != 200:
                raise AssertionError(str(cls.last_response.status_code))
        except ConnectionError as err:
            raise SmokeFailure(
                f"{RED}API Smoke test failed: " + WHITE +
                "Could not connect to server\n" +
                MAGENTA + "  - " + err.request.url + RESET)
        except AssertionError as err:
            raise SmokeFailure(
                f"{RED}API Smoke test failed: {RESET}" +
                "Unexpected return code: " + err)

    @classmethod
    def test_01_smoke_db(cls):
        try:
            cls.GET("/amenities")
            if cls.last_response.status_code != 200:
                raise AssertionError(str(cls.last_response.status_code))
        except ConnectionError as err:
            raise SmokeFailure(
                f"{RED}DB Smoke test failed: " + WHITE +
                "Could not connect to server\n" +
                MAGENTA + "  - " + err.request.url + RESET)
        except AssertionError as err:
            raise SmokeFailure(
                f"{RED}API Smoke test failed: " + WHITE +
                "Unexpected return code: " + MAGENTA + err + RESET)


def run(
        url: str = "http://127.0.0.1:5000/",
        ooe=False,
        results: list = None,
        i: int = None
    ) -> tuple[int, int, int]:
    '''
        Runs all methods of class that start with name test with given url.

        If given a list and an index it dumps the results there too so threads
        can get results.
    '''

    output = TestSmoke.run(url=url, only_output_errors=ooe)
    if results is not None:
        results[i] = output
    return output


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run()
    else:
        url = sys.argv[1]
        run(url)
