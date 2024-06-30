
"""
    DataManager class that implements the iPersistenceManager interface.
    Handles data persistence using JSON files.
"""

import json
import os
import glob

from persistence.data_manager_interface import IPersistenceManager
from logic.model.trackedobject import TrackedObject
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

    def _file_path(self, obj: TrackedObject):
        """
            Creates an obj.
        """

        if obj.id:
            return os.path.join(self.storage_path,
                                f"{obj.__tablename__}_{obj.id}.json")
        else:
            return os.path.join(self.storage_path, f"{obj.__tablename__}.json")

    def create(self, obj: TrackedObject) -> TrackedObject:
        """
            Creates an obj.
        """

        if os.environ.get('USE_DATABASE'):
            db.session
            db.session.add(obj)
            db.session.commit()
            return db.session.query(obj).get(obj.id)
        else:
            file_path = self._file_path(obj, obj.id)
            with open(file_path, 'w') as file:
                json.dump(obj.toJson(), file)

    def read(self, obj: TrackedObject) -> None | TrackedObject:
        """
            Retrieves an obj.
        """

        if os.environ.get('USE_DATABASE'):
            return db.session.query(obj).get(obj.id)
        else:
            file_path = self._file_path(obj, obj.id)
            if not os.path.exists(file_path):
                return None
            else:
                with open(file_path, 'r') as file:
                    ret = obj(**json.load(file))
                return ret

    def update(self, obj: TrackedObject) -> TrackedObject:
        """
            Update an obj.
        """

        if os.environ.get('USE_DATABASE'):
            old_obj = db.session.query(obj).get(obj.id)
            # No se
            db.session.commit()
            return db.session.query(obj).get(obj.id)
        else:
            file_path = self._file_path(obj, obj.id)
            with open(file_path, 'r') as file:
                obj = json.load(file)
                obj.update(obj)

            with open(file_path, 'w') as file:
                json.dump(obj, file)


    def delete(self, obj: TrackedObject) -> None:
        """
            Delete an obj.
        """
        if os.environ.get('USE_DATABASE'):
            row = db.session.query(obj).filter(obj.id == obj.id)
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

    def get_all(self, obj: TrackedObject) -> list[TrackedObject]:
        """
            Retrieves all entities of a given type.
        """

        if os.environ.get('USE_DATABASE'):
            return db.session.query(obj).all()
        else:
            obj
            path = os.path.join(self.storage_path, f"{obj}_*.json")
            files = glob.glob(path)
            entities = []
            for file_path in files:
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        entities.append(data)
            return entities

    def get_by_property(self, obj: TrackedObject,
                        property_name: str, property_value) -> list[dict]:
        """
            Retrieves all entities of a given type that match a specific property
            Attributes:
                obj: the type of entities to retrieve
                property_name: the property name to match
                property_value: the property value to match
            Return: a list of entities that match the given property in JSON
        """
        if os.environ.get('USE_DATABASE'):
            return db.session.query(obj).filter(
                obj.get(property_name) == property_value).all()
        else:
            all_entities = self.get_all(obj)
            matched_entities = [entity for entity in all_entities
                                if entity.get(property_name) == property_value]
            return matched_entities
