#!/usr/bin/python3

'''
    Defines tests for 'reviews' endpoints.
'''

from random import randint
import sys
from uuid import uuid4
from testlib import HTTPTestClass


class TestReviews(HTTPTestClass):
    '''
    Tests:
        ...
    '''

    city_id: str | None = None
    host_id: str | None = None
    amenity_ids: list[str] | None = None
    place_id: str | None = None

    user_id: str | None = None

    review: dict | None = None

    @classmethod
    def createCity(cls, num: int) -> str:
        '''
            Creates city to create place.
        '''

        cls.FROM(f"cities/city_{num}.json")
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

        cls.FROM(f"users/user_{num}.json")
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

        cls.FROM(f"amenities/amenity_{num}.json")
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
        cls.FROM(f"places/place_{num}.json")

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
        cls.place_id = place.get("id")
        cls.amenity_ids = amenity_ids
        cls.host_id = host_id
        cls.city_id = city_id

        return place

    @classmethod
    def createReview(
            cls,
            filenum: int,
            dic: dict | None = None,
            *,
            expected_code: int = 201,
            overrideNone: bool = False
    ) -> dict:

        place_id = cls.createPlace.get("id")
        user_id = cls.createUser(filenum + 1)

        cls.FROM(f"reviews/review_{filenum}.json")

        if dic is not None:
            for key in dic:
                if dic[key] is None or overrideNone:
                    cls.REMOVE_VALUE(key)
                else:
                    cls.SET_VALUE(key, dic[key])

        if expected_code != 201:
            cls.POST("/reviews")
            if cls.last_response.status_code != expected_code:
                if cls.last_response.status_code == 201:
                    cls.deleteAmenity(**cls.GET_RESPONSE_JSON())
                cls._ASSERT(cls.last_response.status_code, expected_code)

        cls.POST("/reviews")

        if cls.last_response.status_code != 201:
            cls.ASSERT_CODE(201)

        review = cls.json.copy()
        review["id"] = cls.GET_RESPONSE_VALUE("id")
        cls.review = review

        return review

    @classmethod
    def deleteReview(
        cls,
        id: str | None = None,
        place_id: str | None = None,
        host_id: str | None = None,
        city_id: str | None = None,
        amenity_ids: list[str] | None = None,
        **kwargs
    ) -> None:
        '''
            Deletes a place using either args or class attributes.
        '''
        if id is None:
            if cls.review is not None:
                id = cls.review.get("id")
        if id is not None:
            cls.DELETE(f"/reviews/{id}")
            cls.review = None
        if place_id is None:
            if cls.place_id is not None:
                place_id = cls.place_id
        if place_id is not None:
            cls.DELETE(f"/users/{host_id}")
            cls.ASSERT_CODE(204)
            cls.place = None
        if host_id is None:
            if cls.host_id is not None:
                host_id = cls.host_id
        if host_id is not None:
            cls.DELETE(f"/users/{host_id}")
            cls.ASSERT_CODE(204)
            cls.host_id = None
        if city_id is None:
            if cls.city_id is not None:
                city_id = cls.city_id
        if city_id is not None:
            cls.DELETE(f"/cities/{city_id}")
            cls.ASSERT_CODE(204)
            cls.city_id = None
        if amenity_ids is None:
            if cls.amenity_ids is not None:
                amenity_ids = cls.amenity_ids
        if amenity_ids is not None:
            for amenity_id in amenity_ids:
                cls.DELETE(f"/amenities/{amenity_id}")
                cls.ASSERT_CODE(204)
            cls.amenity_ids = None

    @classmethod
    def customPUT(
        cls,
        id: str,
        filenum: int = 1,
        dic: dict = {},
        expected_code: int = 200
    ) -> None:
        cls.FROM(f"reviews/review_{filenum}.json")
        for key in dic:
            cls.SET_VALUE(key, dic[key])
        cls.PUT("/reviews/" + id)
        cls.ASSERT_CODE(expected_code)

    @classmethod
    def Teardown(cls):
        cls.deleteReview()

    # Auth as admin

    # 0
    @classmethod
    def test_00_auth(cls):
        cls.AUTH_FROM("admin.json")

    # Valid requests

    # 1
    @classmethod
    def test_01_general_GET(cls):
        cls.GET("/reviews")
        cls.ASSERT_CODE(200)

    # 2
    @classmethod
    def test_02_valid_POST_GET_DELETE(cls):
        for i in range(1, 4):
            amenity = cls.createReview(i)
            cls.deleteAmenity(**amenity)

    # 3
    @classmethod
    def test_03_another_general_GET(cls):
        cls.GET("/reviews")
        cls.ASSERT_CODE(200)

    # 4
    @classmethod
    def test_04_valid_name_PUT(cls):
        for i in range(1, 4):
            amenity = cls.createReview(i)
            cls.SET_VALUE("name", amenity["name"] + "UPDATED")
            cls.PUT("/reviews/" + amenity["id"])
            cls.ASSERT_CODE(200)

    # Empty and invalid requests

    # 5
    @classmethod
    def test_05_all_GET(cls):
        cls.GET("/reviews")
        cls.ASSERT_CODE(200)
        cls.GET("/reviews/")
        cls.ASSERT_CODE(200)
        cls.GET("/reviews/ ")
        cls.ASSERT_CODE(400)
        cls.GET("/reviews/abc")
        cls.ASSERT_CODE(400)
        cls.GET(f"/reviews/{uuid4().hex}")
        cls.ASSERT_CODE(404)

    # 6
    @classmethod
    def test_06_all_DELETE(cls):
        cls.DELETE("/reviews")
        cls.ASSERT_CODE(405)
        cls.DELETE("/reviews/")
        cls.ASSERT_CODE(405)
        cls.DELETE("/reviews/ ")
        cls.ASSERT_CODE(400)
        cls.DELETE("/reviews/abc")
        cls.ASSERT_CODE(400)
        cls.DELETE(f"/reviews/{uuid4().hex}")
        cls.ASSERT_CODE(404)

    # 7
    @classmethod
    def test_07_all_PUT(cls):
        cls.json = {}
        cls.PUT("/reviews")
        cls.ASSERT_CODE(405)
        cls.PUT("/reviews/")
        cls.ASSERT_CODE(405)
        cls.PUT("/reviews/ ")
        cls.ASSERT_CODE(400)
        cls.PUT("/reviews/abc")
        cls.ASSERT_CODE(400)
        cls.PUT(f"/reviews/{uuid4().hex}")
        cls.ASSERT_CODE(400)

    # 8
    @classmethod
    def test_08_invalid_POST(cls):
        cls.json = {}
        cls.POST("/reviews")
        cls.ASSERT_CODE(400)
        cls.POST("/reviews/")
        cls.ASSERT_CODE(400)
        cls.POST("/reviews/ ")
        cls.ASSERT_CODE(405)
        cls.POST("/reviews/abc")
        cls.ASSERT_CODE(405)
        cls.POST(f"/reviews/{uuid4().hex}")
        cls.ASSERT_CODE(405)

    # Invalid fields requests

    # 9
    @classmethod
    def test_09_less_attributes_POST(cls):
        cls.createReview(1, {"name": None}, expected_code=400)

    # 10
    @classmethod
    def test_10_more_attributes_POST(cls):
        cls.createReview(1, {"example": "lechuga"}, expected_code=400)

    # 11
    @classmethod
    def test_11_different_attributes_POST(cls):
        cls.createReview(
            filenum=2,
            dic={"name": None, "example": "pechuga"},
            expected_code=400
        )

    # 12
    @classmethod
    def test_12_less_attributes_PUT(cls):
        amenity = cls.createReview(3)
        cls.REMOVE_VALUE("name")
        cls.PUT("/reviews/" + amenity["id"])
        cls.ASSERT_CODE(400)

    # 13
    @classmethod
    def test_13_more_attributes_PUT(cls):
        amenity = cls.createReview(3)
        cls.SET_VALUE("food", "yes")
        cls.PUT("/reviews/" + amenity["id"])
        cls.ASSERT_CODE(400)

    # 14
    @classmethod
    def test_14_different_attributes_PUT(cls):
        amenity = cls.createReview(3)
        cls.REMOVE_VALUE("name")
        cls.SET_VALUE("food", "yes")
        cls.PUT("/reviews/" + amenity["id"])
        cls.ASSERT_CODE(400)

    # Invalid data requests

    # 15
    @classmethod
    def test_15_invalid_data_POST(cls):
        cls.createReview(1, {"name": ""}, expected_code=400)
        cls.createReview(2, {"name": "    "}, expected_code=400)
        cls.createReview(3, {"name": "\n"}, expected_code=400)
        cls.createReview(1, {"name": "Lechuga🥬"}, expected_code=400)
        cls.createReview(2, {"name": "🗿"}, expected_code=400)
        cls.createReview(3, {"name": "777"}, expected_code=400)

    # 16
    @classmethod
    def test_16_invalid_data_PUT(cls):
        amenity = cls.createReview(1)

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
        cls.createReview(3)
        cls.createReview(3, expected_code=409)

    # 18
    @classmethod
    def test_18_duplicate_entry_PUT(cls):
        amenity_1 = cls.createReview(1)
        amenity_2 = cls.createReview(2)

        cls.FROM("reviews/review_1.json")
        cls.PUT("/reviews/" + amenity_2["id"])
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
        cls.POST("/reviews")
        cls.ASSERT_CODE(403)
        cls.PUT("/reviews/" + uuid4().hex)
        cls.ASSERT_CODE(403)
        cls.DELETE("/reviews/" + uuid4().hex)
        cls.ASSERT_CODE(403)

    # 20
    @classmethod
    def test_20_unaunthentication(cls):
        cls.CLEAN()
        cls.POST("/reviews")
        cls.ASSERT_CODE(401)
        cls.PUT("/reviews/" + uuid4().hex)
        cls.ASSERT_CODE(401)
        cls.DELETE("/reviews/" + uuid4().hex)
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

    output = TestReviews.run(url=url, only_output_errors=ooe)
    if results is not None:
        results[i] = output
    return output


if __name__ == "__main__":
    if len(sys.argv) == 1:
        run()
    else:
        url = sys.argv[1]
        run(url)
