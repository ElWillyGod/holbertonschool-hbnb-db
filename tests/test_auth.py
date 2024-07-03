#!/usr/bin/python3

'''
    Defines tests for authentication and authorization.
'''

import sys
from testlib import HTTPTestClass


class TestAuth(HTTPTestClass):
    '''
        a
    '''

    pass

def run(url: str = "http://127.0.0.1:5000/"):
    TestAuth.CHANGE_URL(url)
    TestAuth.run()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run()
    else:
        run(sys.argv[1])
