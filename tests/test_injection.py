#!/usr/bin/python3

'''
    Defines tests for vulneravilities.
    These tests are not included in the runall due to their nature, as if they
    work or not may not be able to be measured automatically.
'''

import sys
from testlib import HTTPTestClass


class TestInjection(HTTPTestClass):
    '''
        a
    '''

    pass


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

    output = TestInjection.run(url=url, only_output_errors=ooe)
    if results is not None:
        results[i] = output
    return output


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run()
    else:
        url = sys.argv[1]
        run(url)
