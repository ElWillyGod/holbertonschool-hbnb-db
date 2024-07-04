#!/usr/bin/python3

'''
    Defines tests for 'reviews' endpoints.
'''

import sys
from testlib import HTTPTestClass
import asyncio


class TestReviews(HTTPTestClass):
    '''
        #0:  AUTH_FROM admin.json
        #1:  Post-Get review
    '''

    @classmethod
    def Teardown(cls):
        if cls.last_failed and (id_of_last_post := cls.last_post_id):
            cls.DELETE(id_of_last_post)

    @classmethod
    def test_00_auth(cls):
        cls.AUTH_FROM("admin.json")
        cls.ASSERT_CODE(200)

    @classmethod
    def test_1(c):
        pass


async def run(url: str = "http://127.0.0.1:5000/", *, ooe=False):
    '''
        Runs all methods of class that start with name test with given url.
    '''

    return TestReviews.run(url=url, only_output_errors=ooe)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        asyncio.run(run())
    else:
        url = sys.argv[1]
        if url == "gunicorn":
            url = "http://127.0.0.1:8000/"
        asyncio.run(run(url))
