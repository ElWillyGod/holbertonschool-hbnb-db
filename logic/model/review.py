
'''
    Defines the Review class.
    Reviews are linked with a user and a review.
'''

from logic.model.trackedobject import TrackedObject as TObj
from logic.model.user import User
from logic.model.place import Place
from logic import db


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
