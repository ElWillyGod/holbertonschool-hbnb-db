"""
    DataManager class that implements the iPersistenceManager interface.
    SQL
"""

from persistence.data_manager_interface import IPersistenceManager
from typing import Any
from logic import db


class DataManager(IPersistenceManager):


    def create(self, obj) -> Any:
        """
            create register in db
        """
        
        db.session
        db.session.add(obj)
        db.session.commit()

    def read(self, obj) -> None | Any:
        """
            retrievs an obj
        """

        return obj.query.filter_by(id=obj.id).first()


    def update(self, obj) -> Any:
        """
            Update an obj
        """

        old_obj = db.session.query(obj.__class__).get(obj.id)
        for key, value in obj.__dict__.items():
            if not (key.startswith('_') or key == 'created_at'):
                setattr(old_obj, key, value)

        db.session.commit()


    def delete(self, obj) -> None:
        """
            Delete obj
        """

        row = obj.query.filter_by(id=obj.id).first()
        db.session.delete(row)
        db.session.commit()


    def get_all(self, obj_type) -> list[Any]:
        """
            Retrieves all entities of a given type.
        """

        return obj_type.query.all()

    def get_by_property(self, obj_type,
                        property_name: str, property_value) -> list[dict]:
        """
            Retrieves all entities of a given type that match a specific property.
        """

        return obj_type.query.filter_by(**{property_name: property_value}).all()
