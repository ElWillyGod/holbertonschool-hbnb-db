# !/usr/bin/python3

'''
    Defines tests for 'amenities' endpoints.
'''

import sys
from uuid import uuid4
from testlib import HTTPTestClass


class TestAmenities(HTTPTestClass):
    '''
    Tests:
        # 0:  AUTH_FROM admin.json
        # 1:  valid GET all
        # 2:  valid POST, GET, DELETE
        # 3:  valid GET all 2
        # 4:  valid PUT
        # 5:  empty id GET
        # 6:  empty id DELETE
        # 7:  empty id PUT
        # 15: deleted entity GET
        # 16: deleted entity PUT
        # 17: deleted entity DELETE
        # 20: invalid POST, PUT, DELETE
        # 8:  less attr POST
        # 9:  more attr POST
        # 10: diff attr POST
        # 11: less attr PUT
        # 12: more attr PUT
        # 13: diff attr PUT
        # 14: duplicate entity POST
        # 18: empty entity name POST
        # 19: invalid entity POST
        TODO:
        # 14: duplicate entity PUT
        # 21: empty entity name PUT
        # 22: invalid entity PUT
    '''

    @classmethod
    def createAmenity(
            cls,
            num: int,
            dic: dict | None = None,
            *,
            expectAtPOST: int = 201,
            overrideNone: bool = False
    ) -> dict:

        cls.FROM(f"amenities/valid_amenity_{num}.json")

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
    def deleteAmenity(cls, **kwargs):
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
            user = cls.createAmenity(i)
            cls.deleteAmenity(**user)

    # 3
    @classmethod
    def test_03_another_general_GET(cls):
        cls.GET("/amenities")
        cls.ASSERT_CODE(200)

    # 4
    @classmethod
    def test_04_valid_name_PUT(cls):
        for i in range(1, 4):
            user = cls.createAmenity(i)
            cls.SET_VALUE("name", user["name"] + "UPDATED")
            cls.PUT("/amenities/" + user["id"])
            cls.ASSERT_CODE(201)
            cls.deleteAmenity(**user)

    # 5
    @classmethod
    def test_05_empty_id_GET(cls):
        cls.GET("/amenities/")
        cls.ASSERT_CODE(200)
        cls.GET("/amenities/ ")
        cls.ASSERT_CODE(400)

    # 6
    @classmethod
    def test_06_empty_id_DELETE(cls):
        cls.DELETE("/amenities/")
        cls.ASSERT_CODE(405)
        cls.DELETE("/amenities/ ")
        cls.ASSERT_CODE(400)

    # 7
    @classmethod
    def test_07_empty_id_PUT(cls):
        user = cls.createAmenity(1)
        cls.DELETE("/amenities/")
        cls.ASSERT_CODE(405)
        cls.DELETE("/amenities/ ")
        cls.ASSERT_CODE(400)
        cls.deleteAmenity(**user)

    # 15
    @classmethod
    def test_15_id_that_doesnt_exist_GET(cls):
        user = cls.createAmenity(3)
        id = user["id"]
        cls.deleteAmenity(**user)
        cls.GET(f"/amenities/{id}")
        cls.ASSERT_CODE(404)

    # 16
    @classmethod
    def test_16_id_that_doesnt_exist_PUT(cls):
        user = cls.createAmenity(3)
        id = user["id"]
        cls.deleteAmenity(**user)
        cls.PUT(f"/amenities/{id}")
        cls.ASSERT_CODE(404)

    # 17
    @classmethod
    def test_17_id_that_doesnt_exist_DELETE(cls):
        user = cls.createAmenity(3)
        id = user["id"]
        cls.deleteAmenity(**user)
        cls.GET(f"/amenities/{id}")
        cls.ASSERT_CODE(404)

    # 20
    @classmethod
    def test_20_invalid_methods(cls):
        cls.FROM("amenities/valid_amenity_1.json")
        cls.PUT("/amenities")
        cls.ASSERT_CODE(405)
        cls.DELETE("/amenities")
        cls.ASSERT_CODE(405)
        cls.POST(f"/amenities/{uuid4().hex}")
        cls.ASSERT_CODE(405)

    # 8
    @classmethod
    def test_08_less_attributes_POST(cls):
        cls.createAmenity(1, {"name": None}, expectAtPOST=400)

    # 9
    @classmethod
    def test_09_more_attributes_POST(cls):
        cls.createAmenity(1, {"example": "lechuga"}, expectAtPOST=400)

    # 10
    @classmethod
    def test_10_different_attributes_POST(cls):
        cls.createAmenity(
            2,
            {"name": None, "example": "pechuga"},
            expectAtPOST=400
        )

    # 11
    @classmethod
    def test_11_less_attributes_PUT(cls):
        user = cls.createAmenity(3)
        cls.REMOVE_VALUE("name")
        cls.PUT("/amenities/" + user["id"])
        cls.ASSERT_CODE(400)
        cls.deleteAmenity(**user)

    # 12
    @classmethod
    def test_12_more_attributes_PUT(cls):
        user = cls.createAmenity(3)
        cls.SET_VALUE("food", "yes")
        cls.PUT("/amenities/" + user["id"])
        cls.ASSERT_CODE(400)
        cls.deleteAmenity(**user)

    # 13
    @classmethod
    def test_13_different_attributes_PUT(cls):
        user = cls.createAmenity(3)
        cls.REMOVE_VALUE("name")
        cls.SET_VALUE("food", "yes")
        cls.PUT("/amenities/" + user["id"])
        cls.ASSERT_CODE(400)
        cls.deleteAmenity(**user)

    # 14
    @classmethod
    def test_14_duplicate_entry_POST(cls):
        user = cls.createAmenity(3)
        cls.createAmenity(3, expectAtPOST=409)
        cls.deleteAmenity(**user)

    # 18
    @classmethod
    def test_18_empty_name_POST(cls):
        cls.createAmenity(2, {"name": ""}, expectAtPOST=400)
        cls.createAmenity(2, {"name": "    "}, expectAtPOST=400)

    # 19
    @classmethod
    def test_19_invalid_name_POST(cls):
        cls.createAmenity(2, {"name": "\n"}, expectAtPOST=400)
        cls.createAmenity(2, {"name": "Lechuga🥬"}, expectAtPOST=400)
        cls.createAmenity(2, {"name": "🗿"}, expectAtPOST=400)
        cls.createAmenity(2, {"name": "777"}, expectAtPOST=400)


def run(url: str = "http://127.0.0.1:5000/"):
    TestAmenities.CHANGE_URL(url)
    TestAmenities.run()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run()
    else:
        run(sys.argv[1])
