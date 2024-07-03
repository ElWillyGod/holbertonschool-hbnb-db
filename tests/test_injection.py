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

def run(url: str = "http://127.0.0.1:5000/"):
    TestInjection.CHANGE_URL(url)
    TestInjection.run()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run()
    else:
        run(sys.argv[1])
