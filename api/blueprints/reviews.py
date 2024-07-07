
'''
    Reviews endpoints:
        '+': Public, '#': Needs auth, '@': Needs auth and be the same user
             that created it, '-': Needs is_admin = True.

        +GET /users/{user_id}/reviews: Retrieve all reviews written by a
         specific user.

        +GET /places/{place_id}/reviews: Retrieve all reviews for a specific
         place.

        +GET /reviews/{review_id}: Retrieve detailed information about a
         specific review.

        #POST /places/{place_id}/reviews: Create a new review for a specified
         place.

        @PUT /reviews/{review_id}: Update an existing review.

        @DELETE /reviews/{review_id}: Delete a specific review.
    TODO: Reveiw "trying to review own place"
'''

from flask import request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt
from flasgger import swag_from
from logic import logicexceptions
from logic.logicfacade import LogicFacade
import api.validations as val
import api.authlib as authlib
from werkzeug.exceptions import BadRequest, Forbidden, Conflict, NotFound

bp = Blueprint("reviews", __name__)


@bp.get('/users/<user_id>/reviews')
@jwt_required(optional=True)
@swag_from("swagger/reviews/user_get_all.yaml")
def getUserReviews(user_id):
    '''
        Gets all user's reviews.
    '''

    # Checks if it's authorized to make the request.
    if err := authlib.notGetAllAuthorized("user/review", get_jwt()):
        raise Forbidden(err)

    # Check if id is valid.
    if not val.idChecksum(user_id):
        raise BadRequest("Invalid user ID")

    # Calls BL to get all reviews of user.
    try:
        reviews = LogicFacade.getByID(user_id, "reviewUser")
    except (logicexceptions.IDNotFoundError) as err:
        raise NotFound(str(err))

    return reviews, 200


@bp.get('/places/<place_id>/reviews')
@jwt_required(optional=True)
@swag_from("swagger/reviews/place_get_all.yaml")
def getPlaceReviews(place_id):
    '''
        Gets all place's reviews.
    '''

    # Checks if it's authorized to make the request.
    if err := authlib.notGetAllAuthorized("place/review", get_jwt()):
        raise Forbidden(err)

    # Check if id is valid.
    if not val.idChecksum(place_id):
        raise BadRequest("Invalid place ID format")

    # Calls BL to get all reviews of place
    try:
        reviews = LogicFacade.getByID(place_id, 'reviewPlace')
    except (logicexceptions.IDNotFoundError) as err:
        raise NotFound(str(err))

    return reviews, 200


@bp.get('/reviews/<review_id>')
@jwt_required(optional=True)
@swag_from("swagger/reviews/get.yaml")
def getReview(review_id):
    '''
        Gets review.
    '''

    # Checks if it's authorized to make the request.
    if err := authlib.notGetAuthorized("review", get_jwt()):
        raise Forbidden(err)

    # Checks if id is valid.
    if not val.idChecksum(review_id):
        raise BadRequest("Invalid review ID")

    # Calls BL to get review.
    try:
        review = LogicFacade.getByID(review_id, 'review')
    except (logicexceptions.IDNotFoundError) as err:
        raise NotFound(str(err))

    return review, 200


@bp.post('/places/<place_id>/reviews')
@jwt_required(optional=False)
@swag_from("swagger/reviews/post.yaml")
def createReview(place_id):
    '''
        Creates a review.
    '''

    # Checks if it's authorized to make the request.
    if err := authlib.notPostAuthorized("review", get_jwt()):
        raise Forbidden(err)

    # Get data from request.
    data = request.get_json()

    # Check if data is valid.
    if (val.isNoneFields('review', data) or
            not val.idChecksum(place_id) or
            not val.isStrValid('comment')):
        raise BadRequest('Invalid data')

    if not (1 <= data['rating'] <= 5):
        raise BadRequest('Invalid rating')

    data['place_id'] = place_id

    # Calls BL to create review.
    try:
        jwt = get_jwt()
        email = jwt.get("email")
        is_admin = jwt.get("is_admin")
        review = LogicFacade.createObjectByJson(
            'review', data, email, is_admin)
    except logicexceptions.IDNotFoundError as err:
        raise NotFound(str(err))
    except logicexceptions.TryingToReviewOwnPlace as err:
        raise BadRequest(str(err))

    return review, 201


@bp.put('/reviews/<review_id>')
@jwt_required(optional=False)
@swag_from("swagger/reviews/put.yaml")
def updateReview(review_id):
    '''
        Updates a review.
    '''

    # Checks if it's authorized to make the request.
    if err := authlib.notPutAuthorized("amenity", get_jwt()):
        raise Forbidden(err)

    # Get data from request.
    data = request.get_json()

    # Check if data is valid.
    if (val.isNoneFields('review', data) or
            not val.idChecksum(review_id) or
            not val.isStrValid('comment')):
        raise BadRequest('Invalid data')

    if not (1 <= data['rating'] <= 5):
        raise BadRequest('Invalid rating')

    # Calls BL to update review.
    try:
        jwt = get_jwt()
        email = jwt.get("email")
        is_admin = jwt.get("is_admin")
        review = LogicFacade.updateByID(
            review_id, 'review', data, email, is_admin)
    except logicexceptions.IDNotFoundError as err:
        raise NotFound(str(err))
    except logicexceptions.TryingToReviewOwnPlace as err:
        raise BadRequest(str(err))
    except logicexceptions.NotOwner as err:
        raise Forbidden(str(err))

    return review, 200


@bp.delete('/reviews/<review_id>')
@jwt_required(optional=False)
@swag_from("swagger/reviews/delete.yaml")
def deleteReview(review_id):
    '''
        Deletes a review.
    '''

    # Checks if it's authorized to make the request.
    if err := authlib.notDeleteAuthorized("amenity", get_jwt()):
        raise Forbidden(err)

    # Checks if id is valid.
    if not val.idChecksum(review_id):
        raise BadRequest("Invalid review ID format")

    # Calls BL to delete review.
    try:
        jwt = get_jwt()
        email = jwt.get("email")
        is_admin = jwt.get("is_admin")
        LogicFacade.deleteByID(review_id, 'review', email, is_admin)
    except (logicexceptions.IDNotFoundError) as err:
        raise NotFound(str(err))
    except logicexceptions.NotOwner as err:
        raise Forbidden(str(err))

    return "", 204
