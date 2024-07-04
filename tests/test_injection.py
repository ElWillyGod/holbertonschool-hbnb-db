#!/usr/bin/python3

'''
    Defines tests for vulneravilities.
    These tests are not included in the runall due to their nature, as if they
    work or not may not be able to be measured automatically.
'''

import sys
from testlib import HTTPTestClass
import asyncio


class TestInjection(HTTPTestClass):
    '''
        a
    '''

    pass


async def run(url: str = "http://127.0.0.1:5000/", *, ooe=False):
    '''
        Runs all methods of class that start with name test with given url.
    '''

    return TestInjection.run(url=url, only_output_errors=ooe)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        asyncio.run(run())
    else:
        url = sys.argv[1]
        if url == "gunicorn":
            url = "http://127.0.0.1:8000/"
        asyncio.run(run(url))
