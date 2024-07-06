#!/usr/bin/python3

'''
    Defines tests for 'places' endpoints.
'''

from random import randint
import sys
from uuid import uuid4
from testlib import HTTPTestClass


class TestPlaces(HTTPTestClass):
    '''
    ## Amenity tests:
    - Valid requests
        - 0:  AUTH_FROM admin.json
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
        - 15: duplicate POST
        - 17: invalid data POST
        - 18: duplicate PUT
        - 20: invalid data PUT
    - BL requirements tests
        -
    - Authentication and authorization
        - 21: unauthentication on POST, PUT, DELETE
        - 22: unauthorization on POST, PUT, DELETE
    '''

    amenity_ids: list[str] = []
    host_id: str | None = None
    city_id: str | None = None

    place: dict | None = None

    @classmethod
    def createCity(cls, num: int) -> str:
        '''
            Creates city to create place.
        '''

        cls.FROM(f"cities/valid_city_{num}.json")
        cls.POST("/cities")
        cls.ASSERT_CODE(201)
        city_id = cls.GET_RESPONSE_VALUE("id")
        cls.city_id = city_id
        return city_id

    @classmethod
    def createUser(cls, num: int) -> str:
        '''
            Creates user to host place.
        '''

        cls.FROM(f"users/valid_user_{num}.json")
        cls.POST("/users")
        cls.ASSERT_CODE(201)
        user_id = cls.GET_RESPONSE_VALUE("id")
        cls.host_id = user_id
        return user_id

    @classmethod
    def createAmenity(cls, num: int) -> str:
        '''
            Creates amenity to create place.
        '''

        cls.FROM(f"amenities/valid_amenity_{num}.json")
        cls.POST("/amenities")
        cls.ASSERT_CODE(201)
        return cls.GET_RESPONSE_VALUE("id")

    def createAmenities(
            cls,
            number_of_amenities: int | None = None
        ) -> list[str]:
        '''
            Creates multiple amenities and returns a list of their ids.
        '''

        if number_of_amenities is None:
            number_of_amenities = randint(0, 5)
        amenity_ids = []

        available = range(1, 6)
        for _ in range(1, number_of_amenities + 1):
            if len(available) == 0:
                break
            index = randint(0, len(available) - 1)
            num = available.pop(index)
            amenity = cls.createAmenity(num)
            amenity_ids.append(amenity["id"])

        cls.amenity_ids = amenity_ids
        return amenity_ids

    @classmethod
    def createPlace(
        cls,
        num: int,
        number_of_amenities: int | None = None,
        dic: dict | None = None,
        *,
        expectAtPOST: int = 201,
        overrideNone: bool = False
    ) -> dict:
        '''
            Creates a place:
                -> Creates all the necessary objects to create a place.
                -> Creates place using POST.
                -> GETs all places.
                -> Takes created place via name.
                -> Asserts that attributes were assigned successfully.
                -> Returns place w/o created_at or updated_at
        '''

        # Create external objects
        host_id = cls.createUser(num)
        city_id = cls.createCity(num)
        amenity_ids = cls.createAmenities(number_of_amenities)

        # Take dict from json number num
        cls.FROM(f"places/valid_place_{num}.json")

        # Assign ids to place json
        cls.SET_VALUE("host_id", host_id)
        cls.SET_VALUE("city_id", city_id)
        cls.SET_VALUE("amenity_ids", amenity_ids)

        # If dic is passed then override attributes.
        if dic is not None:
            for key in dic:
                if dic[key] is None or overrideNone:
                    cls.REMOVE_VALUE(key)
                else:
                    cls.SET_VALUE(key, dic[key])

        # If expected to fail at POST don't continue
        if expectAtPOST != 201:
            cls.POST("/places")
            if cls.last_response.status_code != expectAtPOST:
                # If 201 delete everything
                if cls.last_response.status_code == 201:
                    cls.deletePlace(**cls.GET_RESPONSE_JSON())
                cls._ASSERT(cls.last_response.status_code, expectAtPOST)

        # POST Place
        cls.POST("/places")

        # If not 201 delete other objects
        if cls.last_response.status_code != 201:
            cls.deletePlace(
                host_id=host_id,
                city_id=city_id,
                amenity_ids=amenity_ids
            )
            cls.ASSERT_CODE(201)

        # Copy response
        place = cls.json.copy()
        place["amenity_ids"] = amenity_ids.copy()  # Deep copy
        place["id"] = cls.GET_RESPONSE_VALUE("id")
        cls.place = place
        cls.amenity_ids = amenity_ids
        cls.host_id = host_id
        cls.city_id = city_id

        return place

    @classmethod
    def deletePlace(
        cls,
        place_id: str | None = None,
        host_id: str | None = None,
        city_id: str | None = None,
        amenity_ids: list[str] | None = None,
        **kwargs
    ) -> None:
        '''
            Deletes a place using either args or class attributes.
        '''

        place_id = place_id if place_id is not None else cls.place.get("id")
        if place_id is not None:
            cls.DELETE(f"/users/{host_id}")
            cls.ASSERT_CODE(204)
            cls.place = None
        host_id = host_id if host_id is not None else cls.host_id
        if host_id is not None:
            cls.DELETE(f"/users/{host_id}")
            cls.ASSERT_CODE(204)
            cls.host_id = None
        city_id = city_id if city_id is not None else cls.city_id
        if city_id is not None:
            cls.DELETE(f"/cities/{city_id}")
            cls.ASSERT_CODE(204)
            cls.city_id = None
        amenity_ids = amenity_ids if amenity_ids else cls.amenity_ids
        if amenity_ids is not None:
            for amenity_id in amenity_ids:
                cls.DELETE(f"/amenities/{amenity_id}")
                cls.ASSERT_CODE(204)
            cls.amenity_ids = None

    @classmethod
    def Teardown(cls):
        cls.deletePlace()

    # 0
    @classmethod
    def test_00_auth(cls):
        cls.AUTH_FROM("admin.json")
        cls.ASSERT_CODE(200)

    # 1
    @classmethod
    def test_01_general_GET(cls):
        cls.GET("/places")
        cls.ASSERT_CODE(200)

    # 2
    @classmethod
    def test_02_valid_POST_GET_DELETE(cls):
        for i in range(1, 4):
            cls.createPlace(i)

    # 3
    @classmethod
    def test_03_another_general_GET(cls):
        cls.GET("/places")
        cls.ASSERT_CODE(200)

    # 4
    @classmethod
    def test_04_description_PUT(cls):
        place = cls.createPlace(1)
        id = place["id"]
        description = "UPDATED"
        cls.SET_VALUE("description", description)
        cls.PUT(f"/places/{id}")
        cls.ASSERT_CODE(200)
        cls.ASSERT_VALUE("description", description)

    # 5
    @classmethod
    def test_05_all_GET(cls):
        cls.GET("/places")
        cls.ASSERT_CODE(200)
        cls.GET("/places/")
        cls.ASSERT_CODE(200)
        cls.GET("/places/ ")
        cls.ASSERT_CODE(400)
        cls.GET("/places/abc")
        cls.ASSERT_CODE(400)
        cls.GET("/places/" + uuid4().hex)
        cls.ASSERT_CODE(404)

    # 6
    @classmethod
    def test_06_all_invalid_PUT(cls):
        cls.json = {}
        cls.PUT("/places/" + uuid4().hex)
        cls.ASSERT_CODE(400)

        cls.PUT("/places")
        cls.ASSERT_CODE(405)
        cls.PUT("/places/")
        cls.ASSERT_CODE(405)
        cls.PUT("/places/ ")
        cls.ASSERT_CODE(400)
        cls.PUT("/places/abc")
        cls.ASSERT_CODE(400)

        cls.createPlace(2)
        cls.PUT("/places/" + uuid4().hex)
        cls.ASSERT_CODE(404)

    # 7
    @classmethod
    def test_07_all_invalid_DELETE(cls):
        cls.DELETE("/places")
        cls.ASSERT_CODE(405)
        cls.DELETE("/places/")
        cls.ASSERT_CODE(405)
        cls.DELETE("/places/ ")
        cls.ASSERT_CODE(400)
        cls.DELETE("/places/abc")
        cls.ASSERT_CODE(400)
        cls.DELETE("/places/" + uuid4().hex)
        cls.ASSERT_CODE(404)

    # 8
    @classmethod
    def test_08_all_invalid_POST(cls):
        cls.json = {}
        cls.POST("/places")
        cls.ASSERT_CODE(400)
        cls.POST("/places/")
        cls.ASSERT_CODE(400)
        cls.POST("/places/ ")
        cls.ASSERT_CODE(405)
        cls.POST("/places/abc")
        cls.ASSERT_CODE(405)
        cls.POST("/places/" + uuid4().hex)
        cls.ASSERT_CODE(405)

    # 9
    @classmethod
    def test_09_less_attributes_POST(cls):
        cls.createPlace(
            1,
            {"name": None},
            expectAtPOST=400
        )
        cls.createPlace(
            2,
            {"description": None},
            expectAtPOST=400
        )
        cls.createPlace(
            3,
            {"latitude": None, "longitude": None},
            expectAtPOST=400
        )
        cls.createPlace(
            1,
            {"host_id": None, "city_id": None},
            expectAtPOST=400
        )
        cls.createPlace(
            2,
            {"amenity_ids": None},
            expectAtPOST=400
        )

    # 10
    @classmethod
    def test_10_more_attributes_POST(cls):
        cls.createPlace(3, {"rating": 100}, expectAtPOST=400)

    # 11
    @classmethod
    def test_11_different_attributes_POST(cls):
        cls.createPlace(
            1,
            {"description": None, "rating": 100},
            expectAtPOST=400
        )
        cls.createPlace(
            2,
            {"name": None, "favorite_fruit": "banana"},
            expectAtPOST=400
        )
        cls.createPlace(
            3,
            {"host_id": None, "explosive_type": "C4"},
            expectAtPOST=400
        )
        cls.createPlace(
            1,
            {"city_id": None, "car": "Toyota"},
            expectAtPOST=400
        )
        cls.createPlace(
            2,
            {"host_id": None, "explosive_type": "C4", "city_id": None,
             "car": "Toyota"},
            expectAtPOST=400
        )

    # 12
    @classmethod
    def test_12_less_attributes_PUT(cls):
        place = cls.createPlace(1)
        id = place["id"]
        cls.REMOVE_VALUE("name")
        cls.PUT(f"/places/{id}")
        cls.ASSERT_CODE(400)
        cls.SET_VALUE("name", place["name"])

        cls.REMOVE_VALUE("host_id")
        cls.PUT(f"/places/{id}")
        cls.ASSERT_CODE(400)
        cls.SET_VALUE("host_id", place["host_id"])

        cls.REMOVE_VALUE("city_id")
        cls.PUT(f"/places/{id}")
        cls.ASSERT_CODE(400)
        cls.SET_VALUE("city_id", place["city_id"])

        cls.REMOVE_VALUE("host_id")
        cls.REMOVE_VALUE("city_id")
        cls.PUT(f"/places/{id}")
        cls.ASSERT_CODE(400)
        cls.SET_VALUE("host_id", place["host_id"])
        cls.SET_VALUE("city_id", place["city_id"])

    # 13
    @classmethod
    def test_13_more_attributes_PUT(cls):
        place = cls.createPlace(2)
        id = place["id"]
        cls.SET_VALUE("rating", 100)
        cls.PUT(f"/places/{id}")
        cls.ASSERT_CODE(400)

    # 14
    @classmethod
    def test_14_different_attributes_PUT(cls):
        place = cls.createPlace(3)
        id = place["id"]
        cls.REMOVE_VALUE("description")
        cls.SET_VALUE("rating", 100)
        cls.PUT(f"/places/{id}")
        cls.ASSERT_CODE(400)
        cls.SET_VALUE("description", place["description"])
        cls.REMOVE_VALUE("rating")

        cls.REMOVE_VALUE("name")
        cls.SET_VALUE("favorite_fruit", "banana")
        cls.PUT(f"/places/{id}")
        cls.ASSERT_CODE(400)
        cls.SET_VALUE("name", place["name"])
        cls.REMOVE_VALUE("favorite_fruit")

        cls.REMOVE_VALUE("host_id")
        cls.SET_VALUE("explosive_type", "C4")
        cls.PUT(f"/places/{id}")
        cls.ASSERT_CODE(400)
        cls.SET_VALUE("host_id", place["host_id"])
        cls.REMOVE_VALUE("explosive_type")

        cls.REMOVE_VALUE("city_id")
        cls.SET_VALUE("car", "Toyota")
        cls.PUT(f"/places/{id}")
        cls.ASSERT_CODE(400)
        cls.SET_VALUE("city_id", place["city_id"])
        cls.REMOVE_VALUE("car")

        cls.REMOVE_VALUE("host_id")
        cls.REMOVE_VALUE("city_id")
        cls.SET_VALUE("explosive_type", "C4")
        cls.SET_VALUE("car", "Toyota")
        cls.PUT(f"/places/{id}")
        cls.ASSERT_CODE(400)
        cls.SET_VALUE("host_id", place["host_id"])
        cls.SET_VALUE("city_id", place["city_id"])
        cls.REMOVE_VALUE("explosive_type")
        cls.REMOVE_VALUE("car")

    # 15
    @classmethod
    def test_15_empty_strings_POST(cls):
        def checkIfEmpty(key):
            cls.createPlace(2, {key: ""}, expectAtPOST=400)
            cls.createPlace(3, {key: "    "}, expectAtPOST=400)

        checkIfEmpty("host_id")
        checkIfEmpty("city_id")
        checkIfEmpty("name")

        cls.createPlace(2, {"amenity_ids": [""]}, expectAtPOST=400)
        cls.createPlace(3, {"amenity_ids": ["    "]}, expectAtPOST=400)

    # 16
    @classmethod
    def test_16_invalid_ints_POST(cls):
        cls.createPlace(1, {"number_of_rooms": -1}, expectAtPOST=400)
        cls.createPlace(2, {"number_of_bathrooms": -1}, expectAtPOST=400)
        cls.createPlace(3, {"max_guests": -1}, expectAtPOST=400)

    # 17
    @classmethod
    def test_17_invalid_floats_POST(cls):
        cls.createPlace(1, {"price_per_night": -1}, expectAtPOST=400)
        cls.createPlace(2, {"price_per_night": 0}, expectAtPOST=400)
        cls.createPlace(2, {"latitude": 120.0}, expectAtPOST=400)
        cls.createPlace(3, {"latitude": -120.0}, expectAtPOST=400)
        cls.createPlace(2, {"longitude": 200.0}, expectAtPOST=400)
        cls.createPlace(3, {"longitude": -200.0}, expectAtPOST=400)

    # 18
    @classmethod
    def test_18_invalid_strings_POST(cls):
        def testStr(key):
            cls.createPlace(1, {key: "\n"}, expectAtPOST=400)
            cls.createPlace(2, {key: "Ex\nmple"}, expectAtPOST=400)
            cls.createPlace(3, {key: "🤔"}, expectAtPOST=400)
            cls.createPlace(1, {key: "Ex🤔mple"}, expectAtPOST=400)

        testStr("host_id")
        testStr("name")
        testStr("city_id")

        cls.createPlace(2, {"host_id": "Fish"}, expectAtPOST=400)
        cls.createPlace(3, {"city_id": "Fish"}, expectAtPOST=400)
        cls.createPlace(1, {"amenity_ids": ["Fish"]}, expectAtPOST=400)
        cls.createPlace(2, {"amenity_ids": ["\n"]}, expectAtPOST=400)
        cls.createPlace(3, {"amenity_ids": ["Ex\nmple"]}, expectAtPOST=400)
        cls.createPlace(1, {"amenity_ids": ["🤔"]}, expectAtPOST=400)
        cls.createPlace(2, {"amenity_ids": ["Ex🤔mple"]}, expectAtPOST=400)

    # 19
    @classmethod
    def test_19_unauthorization(cls):
        cls.CLEAN()
        cls.AUTH_FROM("user.json")
        cls.POST("/places")
        cls.ASSERT_CODE(403)
        cls.PUT("/places/" + uuid4().hex)
        cls.ASSERT_CODE(403)
        cls.DELETE("/places/" + uuid4().hex)
        cls.ASSERT_CODE(403)

    # 20
    @classmethod
    def test_20_unaunthentication(cls):
        cls.CLEAN()
        cls.POST("/places")
        cls.ASSERT_CODE(401)
        cls.PUT("/places/" + uuid4().hex)
        cls.ASSERT_CODE(401)
        cls.DELETE("/places/" + uuid4().hex)
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

    output = TestPlaces.run(url=url, only_output_errors=ooe)
    if results is not None:
        results[i] = output
    return output


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run()
    else:
        url = sys.argv[1]
        run(url)
