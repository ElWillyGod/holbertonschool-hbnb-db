#!/usr/bin/python3

'''
    Run all tests.
'''

import sys
from threading import Thread

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


def run(url: str = "http://127.0.0.1:5000/"):
    '''
        # runall

        Runs smoke, if successful runs all tests asynchronously.

        Try to run server with gunicorn or docker compose if you are going to
        use this function.
    '''

    try:
        results = test_smoke.run(url)
    except test_smoke.SmokeFailure as err:
        @resultsPrint
        def errorPrint():
            print(f"  ! {RED}{err}{RESET}")
        errorPrint()
        return

    info = {
        "tests_failed": results[0],
        "tests_passed": results[1],
        "http_requests": results[2]
    }

    tests = [
        test_amenities.run,
        test_countries.run,
        test_users.run,
        test_cities.run,
        test_places.run,
        test_reviews.run
    ]

    threads: Thread = [None] * len(tests)
    # Results list is passed to be modified as threads don't handle returns
    results: list[tuple[int, int, int]] = [None] * len(tests)

    # Assigns a thread for each test
    for i in range(len(tests)):
        threads[i] = Thread(target=tests[i], args=[url, True, results, i])
        threads[i].start()

    # Waits for tests to finish
    for i in range(len(tests)):
        threads[i].join()

    # Gathers results of tests
    for result in results:
        if result is not None:
            info["tests_failed"] += result[0]
            info["tests_passed"] += result[1]
            info["http_requests"] += result[2]

    # Prints summary
    @resultsPrint
    def successPrint():
        if info['tests_failed'] == 0:
            print(f"  > {GREEN}All ",
                  WHITE, info['tests_passed'], GREEN,
                  " tests passed successully.", RESET, sep="")
        elif info["tests_passed"] == 0:
            print(f"  > {RED}No test from all ",
                  WHITE, info['tests_failed'], RED,
                  " were successful.", RESET, sep="")
        else:
            total_tests = info['tests_failed'] + info['tests_passed']
            print(f"  > {YELLOW}Some tests have failed: ",
                  RESET, sep="")
            print(f"    - {WHITE}{info['tests_failed']} ",
                  YELLOW, "tests failed", RESET, sep="")
            print(f"    - {WHITE}{info['tests_passed']} ",
                  YELLOW, "tests passed", RESET, sep="")
            print(f"    - {WHITE}{total_tests} ",
                  YELLOW, "tests total", RESET, sep="")
        print()
        print(f"  > {MAGENTA}Total HTTP requests: ",
              WHITE, info['http_requests'], RESET, sep="")
    successPrint()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run()
    else:
        run(sys.argv[1])
