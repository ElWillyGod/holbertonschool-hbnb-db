
'''
    Defines the Review class.
    Reviews are linked with a user and a review.
'''

from logic.model.trackedobject import TrackedObject
from logic.model.logicexceptions import NotOwner
from logic.model import classes
from persistence import dm
from logic import db

class Review(TrackedObject, db.Model):
    '''Reviews table'''

    __tablename__ = 'reviews'

    place_id = db.Column(
        db.String(32),
        db.ForeignKey('places.id'),
        nullable=False,
        unique=True
    )
    user_id = db.Column(
        db.String(32),
        db.ForeignKey('users.id'),
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

    def checkThatItCanBeModifiedBy(
            self,
            id: str,
            email: str,
            is_admin: bool = False
    ) -> None:
        if is_admin:
            return
        review: Review = dm.read(Review(id=id))
        user: classes.User = dm.get_by_property(
            classes.User, "email", email)[0]
        if user.id != review.user_id:
            raise NotOwner("not owner of review")
