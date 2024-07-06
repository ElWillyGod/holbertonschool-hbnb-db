
"""
    DataManager class that implements the iPersistenceManager interface.
    Handles data persistence using JSON files.
"""

import json
import os
import glob
from typing import Any

from persistence.data_manager_interface import IPersistenceManager


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

        file_path = self._file_path(obj)
        with open(file_path, 'w') as file:
            json.dump(obj.toJson(), file)

    def read(self, obj) -> None | Any:
        """
            Retrieves an obj.
        """

        file_path = self._file_path(obj)
        if not os.path.exists(file_path):
            return None
        else:
            with open(file_path, 'r') as file:
                data = json.load(file)
                ret = obj.__class__(**data)
            return ret

    def update(self, obj) -> Any:
        """
            Update an obj.
        """

        file_path = self._file_path(obj)
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        for key, value in obj.__dict__.items():
            if not (key.startswith('_') or key == 'created_at'):
                data[key] = value

        with open(file_path, 'w') as file:
            json.dump(data, file)


    def delete(self, obj) -> None:
        """
            Delete an obj.
        """
        file_path = self._file_path(obj)
        if os.path.exists(file_path):
            os.remove(file_path)
            return
        else:
            raise FileNotFoundError(
                    f"No such obj: {obj} with {obj.id}")

    def get_all(self, obj) -> list[Any]:
        """
            Retrieves all entities of a given type.
        """

        path = os.path.join(self.storage_path, f"{obj.__tablename__}_*.json")
        files = glob.glob(path)
        entities = []
        for file_path in files:
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    data = obj.__class__(**data)
                    entities.append(data)
        return entities

    def get_by_property(self, obj,
            property_name: str, property_value) -> list[dict]:
        """
            Retrieves all entities of a given type that match a specific property.
        """

        all_entities = self.get_all(obj)
        matched_entities = [entity for entity in all_entities
                            if entity.get(property_name) == property_value]
        return matched_entities
