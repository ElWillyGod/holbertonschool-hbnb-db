
'''
    Defines smoke test class.

    Tests if nothing awful occurs on execution to save time.
'''
import sys
from testlib import HTTPTestClass

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
        if cls.testsFailed >= 1:
            raise AssertionError()

    @classmethod
    def test_smoke(cls):
        try:
            cls.GET("/countries")
            cls.ASSERT_CODE(200)
        except Exception as err:
            raise AssertionError(f"{RED}Smoke test failed:\n{RESET}  - {err}")


def run(url: str = "http://127.0.0.1:5000/"):
    '''
        Runs all methods of class that start with name with given url.
    '''

    TestSmoke.CHANGE_URL(url)
    return TestSmoke.run()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run()
    else:
        run(sys.argv[1])
