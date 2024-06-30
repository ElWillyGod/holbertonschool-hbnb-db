
'''
    Defines the Review class.
    Reviews are linked with a user and a review.
'''

from logic.model.trackedobject import TrackedObject
from sqlalchemy import Column, Integer, ForeignKey
from logic.model.user import user
from logic.model.city import place


class Review(TrackedObject):
    '''
        Review table.
    '''

    __tablename__ = 'review'
    user_id = Column(Integer, ForeignKey(user.id), nullable=False)
    place_id = Column(Integer, ForeignKey(place.id), nullable=False)
    rating = Column(Integer, nullable=False)

    def __init__(
            self,
            place_id: str,
            user_id: str,
            rating: int,
            comment: str,
            *,
            id: str = None,
            created_at: str = None,
            updated_at: str = None
) -> None:
        super().__init__(id, created_at, updated_at)
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id
        self.comment = comment
