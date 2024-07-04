
'''
    Defines smoke test class.

    Tests if nothing awful occurs on execution to save time.
'''
import sys
from testlib import HTTPTestClass
import asyncio

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
RESET = "\033[0m"


class TestSmoke(HTTPTestClass):
    '''
        Defines smoke test (test if server is up)
    '''

    @classmethod
    def Teardown(cls) -> None:
        if cls.tests_failed >= 1:
            raise AssertionError()

    @classmethod
    def test_smoke_api(cls):
        try:
            cls.GET("/apidocs")
            cls.ASSERT_CODE(200)
        except Exception as err:
            raise AssertionError(
                f"{RED}API Smoke test failed:\n{RESET}  - {err}")

    @classmethod
    def test_smoke_db(cls):
        try:
            cls.GET("/amenities")
            cls.ASSERT_CODE(200)
        except Exception as err:
            raise AssertionError(
                f"{RED}DB Smoke test failed:\n{RESET}  - {err}")


async def run(url: str = "http://127.0.0.1:5000/", *, ooe=False):
    '''
        Runs all methods of class that start with name test with given url.
    '''

    return TestSmoke.run(url=url, only_output_errors=ooe)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        asyncio.run(run())
    else:
        url = sys.argv[1]
        if url == "gunicorn":
            url = "http://127.0.0.1:8000/"
        asyncio.run(run(url))
