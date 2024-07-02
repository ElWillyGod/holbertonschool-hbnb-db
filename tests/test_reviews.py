#!/usr/bin/python3

'''
    Defines tests for 'reviews' endpoints.
'''

import sys
from testlib import HTTPTestClass


class TestReviews(HTTPTestClass):
    '''
        #1: Post-Get review
    '''

    @classmethod
    def test_1(c):
        pass


def run(url: str = "http://127.0.0.1:5000/"):
    TestReviews.CHANGE_URL(url)
    TestReviews.run()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run()
    else:
        run(sys.argv[1])
