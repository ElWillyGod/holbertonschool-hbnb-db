#!/usr/bin/python3

'''
    Defines tests for 'cities' endpoints.
'''

import sys
from uuid import uuid4
from testlib import HTTPTestClass
import asyncio


class TestCities(HTTPTestClass):
    '''
        #0:  AUTH_FROM admin.json
        #1:  Post-Get city
    '''

    @classmethod
    def createCity(
        cls,
        num: int,
        dic: dict | None = None,
        *,
        expectAtPOST: int = 201,
        overrideNone: bool = False
    ) -> dict:
        '''
            Creates a city.
        '''
        cls.FROM(f"cities/valid_city_{num}.json")
        name = cls.GET_VALUE("name")

        if dic is not None:
            for key in dic:
                if dic[key] is None or overrideNone:
                    cls.REMOVE_VALUE(key)
                else:
                    cls.SET_VALUE(key, dic[key])

        if expectAtPOST != 201:
            cls.POST("/cities")
            cls.ASSERT_CODE(expectAtPOST)
            return {}

        cls.POST("/cities")
        cls.ASSERT_CODE(201)

        output = cls.json.copy()
        output["id"] = cls.GET_RESPONSE_VALUE("id")
        return output

    @classmethod
    def deleteCity(cls, **kwargs):
        id = kwargs["id"]
        cls.DELETE(f"/cities/{id}")
        cls.ASSERT_CODE(204)

    @classmethod
    def Teardown(cls):
        if cls.last_failed and (id_of_last_post := cls.last_post_id):
            cls.DELETE(id_of_last_post)

    @classmethod
    def test_00_auth(cls):
        cls.AUTH_FROM("admin.json")
        cls.ASSERT_CODE(200)

    @classmethod
    def test_01_general_GET(cls):
        cls.GET("/cities")
        cls.ASSERT_CODE(200)

    @classmethod
    def test_02_valid_POST_GET_DELETE(cls):
        for i in range(1, 5):
            city = cls.createCity(i)
            cls.deleteCity(**city)

    @classmethod
    def test_03_another_general_GET(cls):
        cls.GET("/cities")
        cls.ASSERT_CODE(200)

    @classmethod
    def test_04_valid_PUT(cls):
        for i in range(1, 5):
            city = cls.createCity(i)
            cls.SET_VALUE("name", city["name"] + "UPDATED")
            cls.PUT("/cities/" + city["id"])
            cls.ASSERT_CODE(201)

    @classmethod
    def test_05_valid_country_code_PUT(cls):
        city = cls.createCity(1)
        cls.SET_VALUE("country_code", "CA")
        cls.PUT("/cities/" + city["id"])
        cls.ASSERT_CODE(201)

    @classmethod
    def test_06_duplicated_entry_POST(cls):
        cls.createCity(2)
        cls.createCity(2, expectAtPOST=409)

    @classmethod
    def test_07_duplicated_entry_PUT(cls):
        city1 = cls.createCity(2)
        city2 = cls.createCity(3)
        cls.SET_VALUE("name", city1["name"])
        cls.SET_VALUE("country_code", city1["country_code"])
        cls.PUT("/cities/" + city2["id"])
        cls.ASSERT_CODE(409)

    @classmethod
    def test_08_empty_id_GET(cls):
        cls.GET("/cities/")
        cls.ASSERT_CODE(404)

    @classmethod
    def test_09_empty_id_DELETE(cls):
        cls.DELETE("/cities/")
        cls.ASSERT_CODE(404)

    @classmethod
    def test_10_empty_id_PUT(cls):
        cls.createCity(4)
        cls.PUT("/cities/")
        cls.ASSERT_CODE(404)

    @classmethod
    def test_11_less_attributes_POST(cls):
        cls.createCity(3, {"name": None}, expectAtPOST=400)
        cls.createCity(4, {"country_code": None}, expectAtPOST=400)

    @classmethod
    def test_12_more_attributes_POST(cls):
        cls.createCity(1, {"favorite_fruit": "banana"}, expectAtPOST=400)

    @classmethod
    def test_13_different_attributes_POST(cls):
        cls.createCity(
            3,
            {"name": None, "favorite_fruit": "banana"},
            expectAtPOST=400
        )
        cls.createCity(
            4,
            {"country_code": None, "favorite_fruit": "banana"},
            expectAtPOST=400
        )
        cls.createCity(
            1,
            {"country_code": None, "name": None, "explosive_type": "C4",
             "favorite_fruit": "banana"},
            expectAtPOST=400
        )

    @classmethod
    def test_14_less_attributes_PUT(cls):
        city = cls.createCity(1)

        cls.REMOVE_VALUE("name")
        cls.PUT("/cities/" + city["id"])
        cls.ASSERT_CODE(400)
        cls.SET_VALUE("name", city["name"])

        cls.REMOVE_VALUE("country_code")
        cls.PUT("/cities/" + city["id"])
        cls.ASSERT_CODE(400)

    @classmethod
    def test_15_more_attributes_PUT(cls):
        city = cls.createCity(2)
        cls.SET_VALUE("favorite_fruit", "banana")
        cls.PUT("/cities/" + city["id"])
        cls.ASSERT_CODE(400)

    @classmethod
    def test_16_different_attributes_PUT(cls):
        city = cls.createCity(3)

        cls.REMOVE_VALUE("name")
        cls.SET_VALUE("favorite_fruit", "banana")
        cls.PUT("/cities/" + city["id"])
        cls.ASSERT_CODE(400)
        cls.REMOVE_VALUE("favorite_fruit")
        cls.SET_VALUE("name", city["name"])

        cls.REMOVE_VALUE("country_code")
        cls.SET_VALUE("explosive_type", "C4")
        cls.PUT("/cities/" + city["id"])
        cls.ASSERT_CODE(400)
        cls.REMOVE_VALUE("explosive_type")
        cls.SET_VALUE("country_code", city["country_code"])

        cls.REMOVE_VALUE("name")
        cls.REMOVE_VALUE("country_code")
        cls.SET_VALUE("favorite_fruit", "banana")
        cls.SET_VALUE("explosive_type", "C4")
        cls.PUT("/cities/" + city["id"])
        cls.ASSERT_CODE(400)

    @classmethod
    def test_17_id_that_doesnt_exist_GET(cls):
        city = cls.createCity(4)
        cls.deleteCity(**city)
        cls.GET(f"/cities/" + city["id"])
        cls.ASSERT_CODE(404)

    @classmethod
    def test_18_id_that_doesnt_exist_PUT(cls):
        city = cls.createCity(1)
        cls.deleteCity(**city)
        cls.PUT(f"/cities/" + city["id"])
        cls.ASSERT_CODE(404)

    @classmethod
    def test_19_id_that_doesnt_exist_DELETE(cls):
        city = cls.createCity(2)
        cls.deleteCity(**city)
        cls.DELETE(f"/cities/" + city["id"])
        cls.ASSERT_CODE(404)

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

    @classmethod
    def test_24_null_args_POST(cls):
        pass

    # 21
    @classmethod
    def test_21_unauthorization(cls):
        cls.FROM("user.json")
        cls.POST("/users")
        cls.ASSERT_CODE(200)
        user = cls.GET_RESPONSE_JSON()

        cls.CLEAN()
        cls.AUTH_FROM("user.json")
        cls.POST("/cities")
        cls.ASSERT_CODE(403)
        cls.PUT("/cities/" + uuid4().hex)
        cls.ASSERT_CODE(403)
        cls.DELETE("/cities/" + uuid4().hex)
        cls.ASSERT_CODE(403)

        cls.DELETE("/users/" + user.get("id"))

    # 22
    @classmethod
    def test_22_unaunthentication(cls):
        cls.CLEAN()
        cls.POST("/cities")
        cls.ASSERT_CODE(401)
        cls.PUT("/cities/" + uuid4().hex)
        cls.ASSERT_CODE(401)
        cls.DELETE("/cities/" + uuid4().hex)
        cls.ASSERT_CODE(401)


async def run(url: str = "http://127.0.0.1:5000/", *, ooe=False):
    '''
        Runs all methods of class that start with name test with given url.
    '''

    return TestCities.run(url=url, only_output_errors=ooe)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        asyncio.run(run())
    else:
        url = sys.argv[1]
        asyncio.run(run(url))
