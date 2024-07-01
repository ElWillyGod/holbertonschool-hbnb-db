
"""
    DataManager class that implements the iPersistenceManager interface.
    Handles data persistence using JSON files.
"""

import json
import os
import glob
from typing import Any

from persistence.data_manager_interface import IPersistenceManager
from logic import db


class DataManager(IPersistenceManager):
    """
        Handles data persistence using JSON files
    """

    def __init__(self, storage_path='data'):
        """
            Initializes the DataManager with a storage path
            Attributes:
                storage_path: The path to the storage directory
        """

        self.storage_path = storage_path
        if not os.path.exists(storage_path):
            os.makedirs(self.storage_path)

    def _file_path(self, obj):
        """
            Creates an obj.
        """

        if obj.id:
            return os.path.join(self.storage_path,
                                f"{obj.__tablename__}_{obj.id}.json")
        else:
            return os.path.join(self.storage_path, f"{obj.__tablename__}.json")

    def create(self, obj) -> Any:
        """
            Creates an obj.
        """

        if os.environ.get('USE_DATABASE'):
            db.session
            db.session.add(obj)
            db.session.commit()
            return db.session.query(obj.__class__).filter_by(id=obj.id).first()
        else:
            file_path = self._file_path(obj, obj.id)
            with open(file_path, 'w') as file:
                json.dump(obj.toJson(), file)

    def read(self, obj) -> None | Any:
        """
            Retrieves an obj.
        """

        if os.environ.get('USE_DATABASE'):
            return db.session.query(obj.__class__).get(obj.id)
        else:
            file_path = self._file_path(obj, obj.id)
            if not os.path.exists(file_path):
                return None
            else:
                with open(file_path, 'r') as file:
                    ret = obj(**json.load(file))
                return ret

    def update(self, obj) -> Any:
        """
            Update an obj.
        """

        if os.environ.get('USE_DATABASE'):
            old_obj = db.session.query(obj.__class__).get(obj.id)
            # No se
            db.session.commit()
            return db.session.query(obj.__class__).get(obj.id)
        else:
            file_path = self._file_path(obj, obj.id)
            with open(file_path, 'r') as file:
                obj = json.load(file)
                obj.update(obj)

            with open(file_path, 'w') as file:
                json.dump(obj, file)


    def delete(self, obj) -> None:
        """
            Delete an obj.
        """
        if os.environ.get('USE_DATABASE'):
            row = db.session.query(obj.__class__).get(obj.id)
            db.session.delete(row)
            db.session.commit()
        else:
            file_path = self._file_path(obj, obj.id)
            if os.path.exists(file_path):
                os.remove(file_path)
                return
            else:
                raise FileNotFoundError(
                    f"No such obj: {obj} with {obj.id}")

    def get_all(self, obj_type) -> list[Any]:
        """
            Retrieves all entities of a given type.
        """

        if os.environ.get('USE_DATABASE'):
            return db.session.query(obj_type).all()
        else:
            obj_type
            path = os.path.join(self.storage_path, f"{obj_type}_*.json")
            files = glob.glob(path)
            entities = []
            for file_path in files:
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        entities.append(data)
            return entities

    def get_by_property(self, obj_type,
            property_name: str, property_value) -> list[dict]:
        """
            Retrieves all entities of a given type that match a specific property.
        """
        if os.environ.get('USE_DATABASE'):
            return obj_type.query.filter_by(**{property_name: property_value}).all()
        else:
            all_entities = self.get_all(obj_type)
            matched_entities = [entity for entity in all_entities
                                if entity.get(property_name) == property_value]
            return matched_entities
