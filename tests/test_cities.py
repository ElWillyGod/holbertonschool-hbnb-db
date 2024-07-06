#!/usr/bin/python3

'''
    Defines tests for 'cities' endpoints.
'''

import sys
from uuid import uuid4
from testlib import HTTPTestClass


class TestCities(HTTPTestClass):
    '''
    ## Amenity tests:
    - Auth as admin
        - 0:  AUTH_FROM admin.json
    - Valid requests
        - 1:  valid GET all
        - 2:  valid POST, GET, DELETE
        - 3:  valid GET all 2
        - 4:  valid PUT
    - Empty and invalid requests
        - 5:  all GET
        - 6:  all invalid DELETE
        - 7:  all invalid PUT
        - 8:  all invalid POST
    - Invalid fields requests
        - 9:  less attr POST
        - 10: more attr POST
        - 11: diff attr POST
        - 12: less attr PUT
        - 13: more attr PUT
        - 14: diff attr PUT
    - Invalid data requests
        - 15: invalid data POST
        - 16: invalid data PUT
    - BL requirements tests
        - 17: duplicate POST
        - 18: duplicate PUT
    - Authentication and authorization
        - 19: unauthentication on POST, PUT, DELETE
        - 20: unauthorization on POST, PUT, DELETE
    '''

    city: dict | None = None

    @classmethod
    def createCity(
            cls,
            filenum: int,
            dic: dict | None = None,
            *,
            expected_code: int = 201,
            overrideNone: bool = False
    ) -> dict:

        cls.FROM(f"cities/valid_city_{filenum}.json")

        if dic is not None:
            for key in dic:
                if dic[key] is None or overrideNone:
                    cls.REMOVE_VALUE(key)
                else:
                    cls.SET_VALUE(key, dic[key])

        if expected_code != 201:
            cls.POST("/cities")
            if cls.last_response.status_code != expected_code:
                if cls.last_response.status_code == 201:
                    cls.deleteCity(**cls.GET_RESPONSE_JSON())
                cls._ASSERT(cls.last_response.status_code, expected_code)

        cls.POST("/cities")

        if cls.last_response.status_code != 201:
            cls.ASSERT_CODE(201)

        amenity = cls.json.copy()
        amenity["id"] = cls.GET_RESPONSE_VALUE("id")
        cls.city = amenity

        return amenity

    @classmethod
    def customPUT(
        cls,
        id: str,
        filenum: int = 1,
        dic: dict = {},
        expected_code: int = 200
    ) -> None:
        cls.FROM(f"cities/valid_city_{filenum}.json")
        for key in dic:
            cls.SET_VALUE(key, dic[key])
        cls.PUT("/cities/" + id)
        cls.ASSERT_CODE(expected_code)

    @classmethod
    def deleteCity(
        cls,
        id: str | None = None,
        **kwargs
    ) -> None:
        if id is None:
            if cls.city is not None:
                id = cls.city.get("id")
        if id is not None:
            cls.DELETE(f"/amenities/{id}")
            cls.city = None

    @classmethod
    def Teardown(cls):
        cls.deleteCity()

    # Auth as admin

    # 0
    @classmethod
    def test_00_auth(cls):
        cls.AUTH_FROM("admin.json")

    # Valid requests

    # 1
    @classmethod
    def test_01_general_GET(cls):
        cls.GET("/cities")
        cls.ASSERT_CODE(200)

    # 2
    @classmethod
    def test_02_valid_POST_GET_DELETE(cls):
        for i in range(1, 4):
            amenity = cls.createCity(i)
            cls.deleteCity(**amenity)

    # 3
    @classmethod
    def test_03_another_general_GET(cls):
        cls.GET("/cities")
        cls.ASSERT_CODE(200)

    # 4
    @classmethod
    def test_04_valid_name_PUT(cls):
        for i in range(1, 4):
            amenity = cls.createCity(i)
            cls.SET_VALUE("name", amenity["name"] + "UPDATED")
            cls.PUT("/cities/" + amenity["id"])
            cls.ASSERT_CODE(200)

    # Empty and invalid requests

    # 5
    @classmethod
    def test_05_all_GET(cls):
        cls.GET("/cities")
        cls.ASSERT_CODE(200)
        cls.GET("/cities/")
        cls.ASSERT_CODE(200)
        cls.GET("/cities/ ")
        cls.ASSERT_CODE(400)
        cls.GET("/cities/abc")
        cls.ASSERT_CODE(400)
        cls.GET(f"/cities/{uuid4().hex}")
        cls.ASSERT_CODE(404)

    # 6
    @classmethod
    def test_06_all_DELETE(cls):
        cls.DELETE("/cities")
        cls.ASSERT_CODE(405)
        cls.DELETE("/cities/")
        cls.ASSERT_CODE(405)
        cls.DELETE("/cities/ ")
        cls.ASSERT_CODE(400)
        cls.DELETE("/cities/abc")
        cls.ASSERT_CODE(400)
        cls.DELETE(f"/cities/{uuid4().hex}")
        cls.ASSERT_CODE(404)

    # 7
    @classmethod
    def test_07_all_PUT(cls):
        cls.json = {}
        cls.PUT("/cities")
        cls.ASSERT_CODE(405)
        cls.PUT("/cities/")
        cls.ASSERT_CODE(405)
        cls.PUT("/cities/ ")
        cls.ASSERT_CODE(400)
        cls.PUT("/cities/abc")
        cls.ASSERT_CODE(400)
        cls.PUT(f"/cities/{uuid4().hex}")
        cls.ASSERT_CODE(400)

    # 8
    @classmethod
    def test_08_invalid_POST(cls):
        cls.json = {}
        cls.POST("/cities")
        cls.ASSERT_CODE(400)
        cls.POST("/cities/")
        cls.ASSERT_CODE(400)
        cls.POST("/cities/ ")
        cls.ASSERT_CODE(405)
        cls.POST("/cities/abc")
        cls.ASSERT_CODE(405)
        cls.POST(f"/cities/{uuid4().hex}")
        cls.ASSERT_CODE(405)

    # Invalid fields requests

    # 9
    @classmethod
    def test_09_less_attributes_POST(cls):
        cls.createCity(1, {"name": None}, expected_code=400)

    # 10
    @classmethod
    def test_10_more_attributes_POST(cls):
        cls.createCity(1, {"example": "lechuga"}, expected_code=400)

    # 11
    @classmethod
    def test_11_different_attributes_POST(cls):
        cls.createCity(
            filenum=2,
            dic={"name": None, "example": "pechuga"},
            expected_code=400
        )

    # 12
    @classmethod
    def test_12_less_attributes_PUT(cls):
        amenity = cls.createCity(3)
        cls.REMOVE_VALUE("name")
        cls.PUT("/cities/" + amenity["id"])
        cls.ASSERT_CODE(400)

    # 13
    @classmethod
    def test_13_more_attributes_PUT(cls):
        amenity = cls.createCity(3)
        cls.SET_VALUE("food", "yes")
        cls.PUT("/cities/" + amenity["id"])
        cls.ASSERT_CODE(400)

    # 14
    @classmethod
    def test_14_different_attributes_PUT(cls):
        amenity = cls.createCity(3)
        cls.REMOVE_VALUE("name")
        cls.SET_VALUE("food", "yes")
        cls.PUT("/cities/" + amenity["id"])
        cls.ASSERT_CODE(400)

    # Invalid data requests

    # 15
    @classmethod
    def test_15_invalid_data_POST(cls):
        cls.createCity(1, {"name": ""}, expected_code=400)
        cls.createCity(2, {"name": "    "}, expected_code=400)
        cls.createCity(3, {"name": "\n"}, expected_code=400)
        cls.createCity(1, {"name": "Lechuga🥬"}, expected_code=400)
        cls.createCity(2, {"name": "🗿"}, expected_code=400)
        cls.createCity(3, {"name": "777"}, expected_code=400)

    # 16
    @classmethod
    def test_16_invalid_data_PUT(cls):
        amenity = cls.createCity(1)

        cls.customPUT(amenity["id"], 1, {"name": ""}, expected_code=400)
        cls.customPUT(amenity["id"], 2, {"name": "    "}, expected_code=400)
        cls.customPUT(amenity["id"], 3, {"name": "\n"}, expected_code=400)
        cls.customPUT(
            amenity["id"], 1, {"name": "Lechuga🥬"}, expected_code=400)
        cls.customPUT(amenity["id"], 2, {"name": "🗿"}, expected_code=400)
        cls.customPUT(amenity["id"], 3, {"name": "777"}, expected_code=400)

    # BL requirements tests

    # 17
    @classmethod
    def test_17_duplicate_entry_POST(cls):
        cls.createCity(3)
        cls.createCity(3, expected_code=409)

    # 18
    @classmethod
    def test_18_duplicate_entry_PUT(cls):
        amenity_1 = cls.createCity(1)
        amenity_2 = cls.createCity(2)

        cls.FROM("cities/valid_city_1.json")
        cls.PUT("/cities/" + amenity_2["id"])
        if cls.last_response.status_code != 409:
            cls.deleteCity(**amenity_1)
            cls.deleteCity(**amenity_2)
        cls.ASSERT_CODE(409)

    @classmethod
    def test_20_empty_name_POST(cls):
        cls.createCity(3, {"name": ""}, expectAtPOST=400)
        cls.createCity(4, {"name": "    "}, expectAtPOST=400)

    @classmethod
    def test_21_empty_country_code_POST(cls):
        cls.createCity(1, {"country_code": ""}, expectAtPOST=400)
        cls.createCity(2, {"country_code": "    "}, expectAtPOST=400)

    @classmethod
    def test_22_invalid_country_code_POST(cls):
        def testPOST(email):
            cls.createCity(3, {"country_code": email}, expectAtPOST=400)

        testPOST("URU")
        testPOST("U")
        testPOST("uy")
        testPOST("10")
        testPOST("U5")
        testPOST("U😀")
        testPOST("😀😀")
        testPOST("😀")

    @classmethod
    def test_23_invalid_name_POST(cls):
        def testPOST(name):
            cls.createCity(4, {"name": name}, expectAtPOST=400)

        testPOST("Lechuga🥬")
        testPOST("777")
        testPOST("Mi\nColon\n")

    @classmethod
    def test_24_null_args_POST(cls):
        cls.createCity(1, {"country_code": None},
                       expectAtPOST=400, overrideNone=True)
        cls.createCity(2, {"name": None},
                       expectAtPOST=400, overrideNone=True)
        cls.createCity(3, {"country_code": None, "name": None},
                       expectAtPOST=400, overrideNone=True)


    # Authentication and authorization

    # 19
    @classmethod
    def test_19_unauthorization(cls):
        cls.CLEAN()
        cls.AUTH_FROM("user.json")
        cls.POST("/cities")
        cls.ASSERT_CODE(403)
        cls.PUT("/cities/" + uuid4().hex)
        cls.ASSERT_CODE(403)
        cls.DELETE("/cities/" + uuid4().hex)
        cls.ASSERT_CODE(403)

    # 20
    @classmethod
    def test_20_unaunthentication(cls):
        cls.CLEAN()
        cls.POST("/cities")
        cls.ASSERT_CODE(401)
        cls.PUT("/cities/" + uuid4().hex)
        cls.ASSERT_CODE(401)
        cls.DELETE("/cities/" + uuid4().hex)
        cls.ASSERT_CODE(401)


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

    output = TestCities.run(url=url, only_output_errors=ooe)
    if results is not None:
        results[i] = output
    return output


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run()
    else:
        url = sys.argv[1]
        run(url)
