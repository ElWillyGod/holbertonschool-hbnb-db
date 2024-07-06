
'''
    Defines the Review class.
    Reviews are linked with a user and a review.
'''

from logic.model.trackedobject import TrackedObject
from logic import db

class Review(TrackedObject, db.Model):

    __tablename__ = 'review'

    place_id = db.Column(db.Integer,
                     db.ForeignKey('place.id'),
                     nullable=False,
                     unique=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False,
        unique=True
    )

    rating = db.Column(db.Integer, nullable=False)

    def __init__(
            self,
            place_id: str = None,
            user_id: str = None,
            rating: int = None,
            comment: str = None,
            *,
            id: str = None,
            created_at: str = None,
            updated_at: str = None
    ) -> None:
        super().__init__(id, created_at, updated_at)
        """
        if not idExists(place_id, "places"):
            raise IDNotFoundError("place_id doesn't pair with a place")
        if not idExists(user_id, "users"):
            raise IDNotFoundError("user_id doesn't pair with a user")
        if isOwnerIDTheSame(place_id, user_id):
            raise TryingToReviewOwnPlace("you cannot review your own place")
            """
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id
        self.comment = comment

"""
class Review(db.Model):
    '''
        Review table.
    '''

    __tablename__ = 'review'
    __ins = TObj()
    id = __ins.id
    created_at = __ins.created_at
    updated_at = __ins.updated_at

    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey(Place.id), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    def toJson(self):
        return {column.name: getattr(self, column.name)
                for column in self.__table__.columns}

"""
