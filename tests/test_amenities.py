# !/usr/bin/python3

'''
    Defines tests for 'amenities' endpoints.
'''

import sys
from uuid import uuid4
from testlib import HTTPTestClass
import asyncio


class TestAmenities(HTTPTestClass):
    '''
    ## Amenity tests:
    - Valid requests
        - 0:  AUTH_FROM admin.json
        - 1:  valid GET all
        - 2:  valid POST, GET, DELETE
        - 3:  valid GET all 2
        - 4:  valid PUT
    - Empty and invalid id requests
        - 5:  invalid id GET
        - 6:  invalid id DELETE
        - 7:  invalid id PUT
    - Invalid fields requests
        - 8: less attr POST
        - 9: more attr POST
        - 10: diff attr POST
        - 11: less attr PUT
        - 12: more attr PUT
        - 13: diff attr PUT
    - Invalid data requests
        - 14: duplicate entity POST
        - 15: empty entity name POST
        - 16: invalid entity POST
        - 17: duplicate entity PUT
        - 18: empty entity name PUT
        - 19: invalid entity PUT
    - Authentication and authorization
        - 20: 
    '''

    @classmethod
    def createAmenity(
            cls,
            filenum: int,
            dic: dict | None = None,
            *,
            expectAtPOST: int = 201,
            overrideNone: bool = False
    ) -> dict:

        cls.FROM(f"amenities/valid_amenity_{filenum}.json")

        if dic is not None:
            for key in dic:
                if dic[key] is None or overrideNone:
                    cls.REMOVE_VALUE(key)
                else:
                    cls.SET_VALUE(key, dic[key])

        if expectAtPOST != 201:
            cls.POST("/amenities")
            cls.ASSERT_CODE(expectAtPOST)
            return {}

        cls.POST("/amenities")
        cls.ASSERT_CODE(201)

        output = cls.json.copy()
        output["id"] = cls.GET_RESPONSE_VALUE("id")
        return output

    @classmethod
    def customPUT(
        cls,
        filenum: int = 1,
        dic: dict = {},
        expectAtPUT: int = 200
    ) -> None:
        cls.FROM(f"amenities/valid_amenity_{filenum}.json")
        for key in dic:
            cls.SET_VALUE(key, dic[key])
        cls.PUT("/amenities")
        cls.ASSERT_CODE(expectAtPUT)

    @classmethod
    def deleteAmenity(cls, **kwargs) -> None:
        id = kwargs["id"]
        cls.DELETE(f"/amenities/{id}")
        cls.ASSERT_CODE(204)

    @classmethod
    def Teardown(cls):
        if cls.last_failed and (id_of_last_post := cls.last_post_id):
            cls.DELETE(id_of_last_post)

    # 0
    @classmethod
    def test_00_auth(cls):
        cls.AUTH_FROM("admin.json")
        cls.ASSERT_CODE(200)

    # 1
    @classmethod
    def test_01_general_GET(cls):
        cls.GET("/amenities")
        cls.ASSERT_CODE(200)

    # 2
    @classmethod
    def test_02_valid_POST_GET_DELETE(cls):
        for i in range(1, 4):
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
        for i in range(1, 4):
            amenity = cls.createAmenity(i)
            cls.SET_VALUE("name", amenity["name"] + "UPDATED")
            cls.PUT("/amenities/" + amenity["id"])
            cls.ASSERT_CODE(204)
            cls.deleteAmenity(**amenity)

    # 5
    @classmethod
    def test_05_all_GET(cls):
        cls.GET("/amenities")
        cls.ASSERT_CODE(200)
        cls.GET("/amenities/")
        cls.ASSERT_CODE(200)
        cls.GET("/amenities/ ")
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
        cls.DELETE(f"/amenities/{uuid4().hex}")
        cls.ASSERT_CODE(404)

    # 7
    @classmethod
    def test_07_all_PUT(cls):
        cls.FROM("amenities/valid_amenity_1.json")
        cls.PUT("/amenities")
        cls.ASSERT_CODE(405)
        cls.PUT("/amenities/")
        cls.ASSERT_CODE(405)
        cls.PUT("/amenities/ ")
        cls.ASSERT_CODE(400)
        cls.PUT(f"/amenities/{uuid4().hex}")
        cls.ASSERT_CODE(404)

    # 8
    @classmethod
    def test_08_invalid_POST(cls):
        cls.FROM("amenities/valid_amenity_1.json")
        cls.POST("/amenities/ ")
        cls.ASSERT_CODE(405)
        cls.POST(f"/amenities/{uuid4().hex}")
        cls.ASSERT_CODE(405)

    # 9
    @classmethod
    def test_09_less_attributes_POST(cls):
        cls.createAmenity(1, {"name": None}, expectAtPOST=400)

    # 10
    @classmethod
    def test_10_more_attributes_POST(cls):
        cls.createAmenity(1, {"example": "lechuga"}, expectAtPOST=400)

    # 11
    @classmethod
    def test_11_different_attributes_POST(cls):
        cls.createAmenity(
            2,
            {"name": None, "example": "pechuga"},
            expectAtPOST=400
        )

    # 12
    @classmethod
    def test_12_less_attributes_PUT(cls):
        amenity = cls.createAmenity(3)
        cls.REMOVE_VALUE("name")
        cls.PUT("/amenities/" + amenity["id"])
        cls.ASSERT_CODE(400)
        cls.deleteAmenity(**amenity)

    # 13
    @classmethod
    def test_13_more_attributes_PUT(cls):
        amenity = cls.createAmenity(3)
        cls.SET_VALUE("food", "yes")
        cls.PUT("/amenities/" + amenity["id"])
        cls.ASSERT_CODE(400)
        cls.deleteAmenity(**amenity)

    # 14
    @classmethod
    def test_14_different_attributes_PUT(cls):
        amenity = cls.createAmenity(3)
        cls.REMOVE_VALUE("name")
        cls.SET_VALUE("food", "yes")
        cls.PUT("/amenities/" + amenity["id"])
        cls.ASSERT_CODE(400)
        cls.deleteAmenity(**amenity)

    # 15
    @classmethod
    def test_15_duplicate_entry_POST(cls):
        amenity = cls.createAmenity(3)
        cls.createAmenity(3, expectAtPOST=409)
        cls.deleteAmenity(**amenity)

    # 16
    @classmethod
    def test_16_empty_name_POST(cls):
        cls.createAmenity(2, {"name": ""}, expectAtPOST=400)
        cls.createAmenity(2, {"name": "    "}, expectAtPOST=400)

    # 17
    @classmethod
    def test_17_invalid_name_POST(cls):
        cls.createAmenity(2, {"name": "\n"}, expectAtPOST=400)
        cls.createAmenity(2, {"name": "Lechuga🥬"}, expectAtPOST=400)
        cls.createAmenity(2, {"name": "🗿"}, expectAtPOST=400)
        cls.createAmenity(2, {"name": "777"}, expectAtPOST=400)

    # 18
    @classmethod
    def test_18_duplicate_entry_PUT(cls):
        amenity = cls.createAmenity(3)

        cls.customPUT(3, expectAtPUT=409)

        cls.deleteAmenity(**amenity)

    # 19
    @classmethod
    def test_19_empty_name_PUT(cls):
        amenity = cls.createAmenity(1)

        cls.customPUT(1, {"name": ""}, expectAtPUT=400)
        cls.customPUT(1, {"name": "    "}, expectAtPUT=400)

        cls.deleteAmenity(**amenity)

    # 20
    @classmethod
    def test_20_invalid_name_PUT(cls):
        amenity = cls.createAmenity(1)

        cls.customPUT(2, {"name": "\n"}, expectAtPUT=400)
        cls.customPUT(2, {"name": "Lechuga🥬"}, expectAtPUT=400)
        cls.customPUT(2, {"name": "🗿"}, expectAtPUT=400)
        cls.customPUT(2, {"name": "777"}, expectAtPUT=400)

        cls.deleteAmenity(**amenity)


async def run(url: str = "http://127.0.0.1:5000/", *, ooe=False):
    '''
        Runs all methods of class that start with name test with given url.
    '''

    return TestAmenities.run(url=url, only_output_errors=ooe)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        asyncio.run(run())
    else:
        url = sys.argv[1]
        if url == "gunicorn":
            url = "http://127.0.0.1:8000/"
        asyncio.run(run(url))
