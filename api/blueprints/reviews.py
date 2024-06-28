
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
'''

from flask import request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt
from logic import logicexceptions
from logic.logicfacade import LogicFacade
import api.validations as val
import api.authlib as authlib

bp = Blueprint("reviews", __name__)


@bp.get('/users/<user_id>/reviews')
@jwt_required(optional=True)
def getUserReviews(user_id):
    """
    Retrieve all reviews written by a specific user.
    ---
    tags:
      - reviews
    parameters:
      - in: path
        name: user_id
        type: string
        required: true
        description: ID of the user whose reviews are to be retrieved
    responses:
      200:
        description: List of reviews written by the user
      400:
        description: Invalid user ID format
      404:
        description: User ID not found or no reviews found for the user
    """

    # Checks if it's authorized to make the request.
    if err := authlib.notGetAllAuthorized("user/review", get_jwt()):
        return err, 403

    # Check if id is valid.
    if not val.idChecksum(user_id):
        return {'error': "Invalid user ID"}, 400

    # Calls BL to get all reviews of user.
    try:
        reviews = LogicFacade.getByID(user_id, "reviewUser")
    except (logicexceptions.IDNotFoundError) as err:
        return {'error': str(err)}, 404

    return reviews, 200


@bp.get('/places/<place_id>/reviews')
@jwt_required(optional=True)
def getPlaceReviews(place_id):
    """
    Retrieve all reviews for a specific place.
    ---
    tags:
      - reviews
    parameters:
      - in: path
        name: place_id
        type: string
        required: true
        description: ID of the place whose reviews are to be retrieved
    responses:
      200:
        description: List of reviews for the place
      400:
        description: Invalid place ID format
      404:
        description: Place ID not found or no reviews found for the place
    """

    # Checks if it's authorized to make the request.
    if err := authlib.notGetAllAuthorized("place/review", get_jwt()):
        return err, 403

    # Check if id is valid.
    if not val.idChecksum(place_id):
        return {'error': "Invalid place ID format"}, 400

    # Calls BL to get all reviews of place
    try:
        reviews = LogicFacade.getByID(place_id, 'reviewPlace')
    except (logicexceptions.IDNotFoundError) as err:
        return {'error': str(err)}, 404

    return reviews, 200


@bp.get('/reviews/<review_id>')
@jwt_required(optional=True)
def getReview(review_id):
    """
    Retrieve detailed information about a specific review.
    ---
    tags:
      - reviews
    parameters:
      - in: path
        name: review_id
        type: string
        required: true
        description: ID of the review to retrieve
    responses:
      200:
        description: Detailed information about the review
      400:
        description: Invalid review ID format
      404:
        description: Review ID not found
    """

    # Checks if it's authorized to make the request.
    if err := authlib.notGetAuthorized("review", get_jwt()):
        return err, 403

    # Checks if id is valid.
    if not val.idChecksum(review_id):
        return {'error': "Invalid review ID"}, 400

    # Calls BL to get review.
    try:
        review = LogicFacade.getByID(review_id, 'review')
    except (logicexceptions.IDNotFoundError) as err:
        return {'error': str(err)}, 404

    return review, 200


@bp.post('/places/<place_id>/reviews')
@jwt_required(optional=False)
def createReview(place_id):
    """
    Create a new review for a specified place.
    ---
    tags:
      - reviews
    parameters:
      - in: path
        name: place_id
        type: string
        required: true
        description: ID of the place to review
      - in: body
        name: review
        required: true
        schema:
          type: object
          properties:
            rating:
              type: integer
              description: Rating for the place (1 to 5)
              example: 5
            comment:
              type: string
              description: Optional comment about the place
              example: muy bueno
    responses:
      201:
        description: Review created successfully
      400:
        description: Invalid request data or missing fields
      404:
        description: Place ID not found or trying to review own place
    """

    # Checks if it's authorized to make the request.
    if err := authlib.notPostAuthorized("review", get_jwt()):
        return err, 403

    # Get data from request.
    data = request.get_json()

    # Check if data is valid.
    if (val.isNoneFields('review', data) or
            not val.idChecksum(place_id) or
            not val.isStrValid('comment')):
        return {'error': 'Invalid data'}, 400

    if not (1 <= data['rating'] <= 5):
        return {'error': 'Invalid rating'}, 400

    data['place_id'] = place_id

    # Calls BL to create review.
    try:
        review = LogicFacade.createObjectByJson('review', data)
    except (logicexceptions.IDNotFoundError) as err:
        return {'error': str(err)}, 404
    except (logicexceptions.TryingToReviewOwnPlace) as err:
        return {'error': str(err)}, 400

    return review, 201


@bp.put('/reviews/<review_id>')
@jwt_required(optional=False)
def updateReview(review_id):
    """
    Update an existing review.
    ---
    tags:
      - reviews
    parameters:
      - in: path
        name: review_id
        type: string
        required: true
        description: ID of the review to update
      - in: body
        name: review
        required: true
        schema:
          type: object
          properties:
            rating:
              type: integer
              description: Updated rating for the review (1 to 5)
            comment:
              type: string
              description: Updated comment for the review
    responses:
      200:
        description: Review updated successfully
      400:
        description: Invalid request data or missing fields
      404:
        description: Review ID not found or trying to update own review
    """

    # Checks if it's authorized to make the request.
    if err := authlib.notPutAuthorized("amenity", get_jwt()):
        return err, 403

    # Get data from request.
    data = request.get_json()

    # Check if data is valid.
    if (val.isNoneFields('review', data) or
            not val.idChecksum(review_id) or
            not val.isStrValid('comment')):
        return {'error': 'Invalid data'}, 400

    if not (1 <= data['rating'] <= 5):
        return {'error': 'Invalid rating'}, 400

    # Calls BL to update review.
    try:
        review = LogicFacade.updateByID(
            review_id, 'review', data, user=get_jwt())
    except (logicexceptions.IDNotFoundError) as err:
        return {'error': str(err)}, 404
    except (logicexceptions.TryingToReviewOwnPlace) as err:
        return {'error': str(err)}, 400

    return review, 200


@bp.delete('/reviews/<review_id>')
@jwt_required(optional=False)
def deleteReview(review_id):
    """
    Delete a specific review.
    ---
    tags:
      - reviews
    parameters:
      - in: path
        name: review_id
        type: string
        required: true
        description: ID of the review to delete
    responses:
      204:
        description: Review deleted successfully
      400:
        description: Invalid review ID format
      404:
        description: Review ID not found
    """

    # Checks if it's authorized to make the request.
    if err := authlib.notDeleteAuthorized("amenity", get_jwt()):
        return err, 403

    # Checks if id is valid.
    if not val.idChecksum(review_id):
        return {'error': "Invalid review ID format"}, 400

    # Calls BL to delete review.
    try:
        LogicFacade.deleteByID(review_id, 'review', user=get_jwt())
    except (logicexceptions.IDNotFoundError) as err:
        return {'error': str(err)}, 404

    return "", 204
