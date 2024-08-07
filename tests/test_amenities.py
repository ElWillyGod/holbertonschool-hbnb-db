#!/usr/bin/python3

'''
    Defines tests for 'amenities' endpoints.
'''

import sys
from uuid import uuid4
from testlib import HTTPTestClass


class TestAmenities(HTTPTestClass):
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

    amenity: dict | None = None

    @classmethod
    def createAmenity(
            cls,
            filenum: int,
            dic: dict | None = None,
            *,
            expected_code: int = 201,
            overrideNone: bool = False
    ) -> dict:

        cls.FROM(f"amenities/amenity_{filenum}.json")

        if dic is not None:
            for key in dic:
                if dic[key] is None or overrideNone:
                    cls.REMOVE_VALUE(key)
                else:
                    cls.SET_VALUE(key, dic[key])

        if expected_code != 201:
            cls.POST("/amenities")
            if cls.last_response.status_code != expected_code:
                if cls.last_response.status_code == 201:
                    cls.deleteAmenity(**cls.GET_RESPONSE_JSON())
                cls._ASSERT(cls.last_response.status_code, expected_code)

        cls.POST("/amenities")

        if cls.last_response.status_code != 201:
            cls.ASSERT_CODE(201)

        amenity = cls.json.copy()
        amenity["id"] = cls.GET_RESPONSE_VALUE("id")
        cls.amenity = amenity

        return amenity

    @classmethod
    def customPUT(
        cls,
        id: str,
        filenum: int = 1,
        dic: dict = {},
        expected_code: int = 200
    ) -> None:
        cls.FROM(f"amenities/amenity_{filenum}.json")
        for key in dic:
            cls.SET_VALUE(key, dic[key])
        cls.PUT("/amenities/" + id)
        cls.ASSERT_CODE(expected_code)

    @classmethod
    def deleteAmenity(
        cls,
        id: str | None = None,
        **kwargs
    ) -> None:
        if id is None:
            if cls.amenity is not None:
                id = cls.amenity.get("id")
        if id is not None:
            cls.DELETE(f"/amenities/{id}")
            cls.amenity = None

    @classmethod
    def Teardown(cls):
        cls.deleteAmenity()

    # Auth as admin

    # 0
    @classmethod
    def test_00_auth(cls):
        cls.AUTH_FROM("admin.json")

    # Valid requests

    # 1
    @classmethod
    def test_01_general_GET(cls):
        cls.GET("/amenities")
        cls.ASSERT_CODE(200)

    # 2
    @classmethod
    def test_02_valid_POST_GET_DELETE(cls):
        for i in range(1, 6):
            amenity = cls.createAmenity(i)
            cls.deleteAmenity(**amenity)

    # 3
    @classmethod
    def test_03_another_general_GET(cls):
        cls.GET("/amenities")
        cls.ASSERT_CODE(200)

    # 4
    @classmethod
    def test_04_valid_name_PUT(cls):
        for i in range(1, 6):
            amenity = cls.createAmenity(i)
            cls.SET_VALUE("name", amenity["name"] + "UPDATED")
            cls.PUT("/amenities/" + amenity["id"])
            cls.ASSERT_CODE(200)

    # Empty and invalid requests

    # 5
    @classmethod
    def test_05_all_GET(cls):
        cls.GET("/amenities")
        cls.ASSERT_CODE(200)
        cls.GET("/amenities/")
        cls.ASSERT_CODE(200)
        cls.GET("/amenities/ ")
        cls.ASSERT_CODE(400)
        cls.GET("/amenities/abc")
        cls.ASSERT_CODE(400)
        cls.GET(f"/amenities/{uuid4().hex}")
        cls.ASSERT_CODE(404)

    # 6
    @classmethod
    def test_06_all_DELETE(cls):
        cls.DELETE("/amenities")
        cls.ASSERT_CODE(405)
        cls.DELETE("/amenities/")
        cls.ASSERT_CODE(405)
        cls.DELETE("/amenities/ ")
        cls.ASSERT_CODE(400)
        cls.DELETE("/amenities/abc")
        cls.ASSERT_CODE(400)
        cls.DELETE(f"/amenities/{uuid4().hex}")
        cls.ASSERT_CODE(404)

    # 7
    @classmethod
    def test_07_all_PUT(cls):
        cls.json = {}
        cls.PUT("/amenities")
        cls.ASSERT_CODE(405)
        cls.PUT("/amenities/")
        cls.ASSERT_CODE(405)
        cls.PUT("/amenities/ ")
        cls.ASSERT_CODE(400)
        cls.PUT("/amenities/abc")
        cls.ASSERT_CODE(400)
        cls.PUT(f"/amenities/{uuid4().hex}")
        cls.ASSERT_CODE(400)

    # 8
    @classmethod
    def test_08_invalid_POST(cls):
        cls.json = {}
        cls.POST("/amenities")
        cls.ASSERT_CODE(400)
        cls.POST("/amenities/")
        cls.ASSERT_CODE(400)
        cls.POST("/amenities/ ")
        cls.ASSERT_CODE(405)
        cls.POST("/amenities/abc")
        cls.ASSERT_CODE(405)
        cls.POST(f"/amenities/{uuid4().hex}")
        cls.ASSERT_CODE(405)

    # Invalid fields requests

    # 9
    @classmethod
    def test_09_less_attributes_POST(cls):
        cls.createAmenity(1, {"name": None}, expected_code=400)

    # 10
    @classmethod
    def test_10_more_attributes_POST(cls):
        cls.createAmenity(1, {"example": "lechuga"}, expected_code=400)

    # 11
    @classmethod
    def test_11_different_attributes_POST(cls):
        cls.createAmenity(
            filenum=2,
            dic={"name": None, "example": "pechuga"},
            expected_code=400
        )

    # 12
    @classmethod
    def test_12_less_attributes_PUT(cls):
        amenity = cls.createAmenity(3)
        cls.REMOVE_VALUE("name")
        cls.PUT("/amenities/" + amenity["id"])
        cls.ASSERT_CODE(400)

    # 13
    @classmethod
    def test_13_more_attributes_PUT(cls):
        amenity = cls.createAmenity(3)
        cls.SET_VALUE("food", "yes")
        cls.PUT("/amenities/" + amenity["id"])
        cls.ASSERT_CODE(400)

    # 14
    @classmethod
    def test_14_different_attributes_PUT(cls):
        amenity = cls.createAmenity(3)
        cls.REMOVE_VALUE("name")
        cls.SET_VALUE("food", "yes")
        cls.PUT("/amenities/" + amenity["id"])
        cls.ASSERT_CODE(400)

    # Invalid data requests

    # 15
    @classmethod
    def test_15_invalid_data_POST(cls):
        cls.createAmenity(1, {"name": ""}, expected_code=400)
        cls.createAmenity(2, {"name": "    "}, expected_code=400)
        cls.createAmenity(3, {"name": "\n"}, expected_code=400)
        cls.createAmenity(1, {"name": "Lechuga🥬"}, expected_code=400)
        cls.createAmenity(2, {"name": "🗿"}, expected_code=400)
        cls.createAmenity(3, {"name": "777"}, expected_code=400)

    # 16
    @classmethod
    def test_16_invalid_data_PUT(cls):
        amenity = cls.createAmenity(1)

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
        cls.createAmenity(3)
        cls.createAmenity(3, expected_code=409)

    # 18
    @classmethod
    def test_18_duplicate_entry_PUT(cls):
        amenity_1 = cls.createAmenity(1)
        amenity_2 = cls.createAmenity(2)

        cls.FROM("amenities/amenity_1.json")
        cls.PUT("/amenities/" + amenity_2["id"])
        if cls.last_response.status_code != 409:
            cls.deleteAmenity(**amenity_1)
            cls.deleteAmenity(**amenity_2)
        cls.ASSERT_CODE(409)

    # Authentication and authorization

    # 19
    @classmethod
    def test_19_unauthorization(cls):
        cls.CLEAN()
        cls.AUTH_FROM("user.json")
        cls.POST("/amenities")
        cls.ASSERT_CODE(403)
        cls.PUT("/amenities/" + uuid4().hex)
        cls.ASSERT_CODE(403)
        cls.DELETE("/amenities/" + uuid4().hex)
        cls.ASSERT_CODE(403)

    # 20
    @classmethod
    def test_20_unaunthentication(cls):
        cls.CLEAN()
        cls.POST("/amenities")
        cls.ASSERT_CODE(401)
        cls.PUT("/amenities/" + uuid4().hex)
        cls.ASSERT_CODE(401)
        cls.DELETE("/amenities/" + uuid4().hex)
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

    output = TestAmenities.run(url=url, only_output_errors=ooe)
    if results is not None:
        results[i] = output
    return output


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run()
    else:
        url = sys.argv[1]
        run(url)
