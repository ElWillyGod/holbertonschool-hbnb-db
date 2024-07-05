#!/usr/bin/python3

'''
    Run all tests.
'''

import sys
import asyncio

import test_smoke
import test_amenities
import test_countries
import test_users
import test_cities
import test_places
import test_reviews

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
WHITE = "\033[37m"
FAINT = "\033[2m"
RESET = "\033[0m"
INTENSITY_RESET = "\033[22m"


def resultsPrint(middle: callable) -> None:
    '''
        Prints results in a fancy manner.
    '''

    def inner():
        print()
        print(FAINT, "|" * 32, RESET)
        print()
        middle()
        print()
        print(FAINT, "|" * 32, RESET)
        print()

    return inner


async def run(url: str = "http://127.0.0.1:5000/"):
    '''
        # runall

        Runs smoke, if successful runs all tests asynchronously.

        Try to run server with gunicorn or docker compose if you are going to
        use this function.
    '''

    try:
        results = await test_smoke.run(url)
    except test_smoke.SmokeFailure as err:
        @resultsPrint
        def errorPrint():
            print(f"  ! {RED}{err}{RESET}")
        errorPrint()
        return
    tests = {
        "tests_failed": results[0],
        "tests_passed": results[1],
        "http_requests": results[2]
    }

    results = asyncio.gather(
        test_amenities.run(url),
        test_countries.run(url),
        test_users.run(url),
        test_cities.run(url),
        test_places.run(url),
        test_reviews.run(url)
    )

    for tuple in results:
        tests["tests_failed"] += tuple[0]
        tests["tests_passed"] += tuple[1]
        tests["http_requests"] += tuple[2]

    @resultsPrint
    def successPrint():
        if tests['tests_failed'] == 0:
            print(f"  > {GREEN}All ",
                  WHITE, tests['tests_passed'], GREEN,
                  "passed successully.")
        elif tests["tests_passed"] == 0:
            print(f"  > {RED}No test from all ",
                  WHITE, tests['tests_failed'], RED,
                  "were successful.", RESET)
        else:
            total_tests = tests['tests_failed'] + tests['tests_passed']
            print(f"  > {YELLOW}Some tests have failed: ")
            print(f"    - {WHITE}{tests['tests_failed']} ",
                  YELLOW, "tests failed", RESET)
            print(f"    - {WHITE}{tests['tests_passed']} ",
                  YELLOW, "tests passed", RESET)
            print(f"    - {WHITE}{total_tests} ",
                  YELLOW, "tests total", RESET)
        print()
        print(f"  > {MAGENTA} Total HTTP requests: ",
              WHITE, tests['http_requests'], RESET)
    successPrint()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        asyncio.run(run())
    else:
        asyncio.run(run(sys.argv[1]))
