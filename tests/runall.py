#!/usr/bin/python3

'''
    Run all tests.
'''

import sys

import test_smoke
import test_amenities
import test_countries
import test_users
import test_cities
import test_places
import test_reviews


def run(url: str = "http://127.0.0.1:5000/"):
    '''
        Run smoke, if successful run all tests.
    '''

    test_smoke.run(url)
    test_amenities.run(url)
    test_countries.run(url)
    test_users.run(url)
    test_cities.run(url)
    test_places.run(url)
    test_reviews.run(url)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run()
    else:
        run(sys.argv[1])
