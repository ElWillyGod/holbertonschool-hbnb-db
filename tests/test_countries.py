#!/usr/bin/python3

'''
    Defines tests for 'Countries' endpoints.
'''

import sys
from testlib import HTTPTestClass
import asyncio


class TestCountries(HTTPTestClass):
    '''
        #1: Test country get.
    '''

    @classmethod
    def test_01_general_GET(cls):
        cls.GET("/countries")
        cls.ASSERT_CODE(200)

        cls.ASSERT_VALUE("code", "UY")
        cls.ASSERT_VALUE("name", "Uruguay")

        cls.ASSERT_VALUE("code", "AR")
        cls.ASSERT_VALUE("name", "Argentina")

        cls.ASSERT_VALUE("code", "ES")
        cls.ASSERT_VALUE("name", "Spain")

        cls.ASSERT_VALUE("code", "US")
        cls.ASSERT_VALUE("name", "United States")

        cls.ASSERT_VALUE("code", "BR")
        cls.ASSERT_VALUE("name", "Brazil")


async def run(url: str = "http://127.0.0.1:5000/", *, ooe=False):
    '''
        Runs all methods of class that start with name test with given url.
    '''

    return TestCountries.run(url=url, only_output_errors=ooe)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        asyncio.run(run())
    else:
        url = sys.argv[1]
        asyncio.run(run(url))
