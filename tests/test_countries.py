#!/usr/bin/python3

'''
    Defines tests for 'Countries' endpoints.
'''

import sys
from testlib import HTTPTestClass


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

    output = TestCountries.run(url=url, only_output_errors=ooe)
    if results is not None:
        results[i] = output
    return output


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run()
    else:
        url = sys.argv[1]
        run(url)
