
"""
    Data manager
    Handles:
        Save
        Get
        Update
        Delete
        Get all
        Get by property
        Get countries
"""

from abc import abstractmethod, ABC


class IPersistenceManager(ABC):

    @abstractmethod
    def create(self, obj):
        pass
    
    @abstractmethod
    def read(self, obj):
        pass

    @abstractmethod
    def update(self, obj):
        pass

    @abstractmethod
    def delete(self, obj):
        pass

    @abstractmethod
    def get_all(self, obj_type):
        pass

    @abstractmethod
    def get_by_property(self, obj_type, property_name, property_value):
        pass
