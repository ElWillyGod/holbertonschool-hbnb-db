
'''
    Warning: Changes to classes may affect all layers.
'''

from logic.model.user import User
from logic.model.city import City
from logic.model.country import Country
from logic.model.amenity import Amenity
from logic.model.place import Place
from logic.model.review import Review


classes = [
           ["user", User],
           ["city", City],
           ["country", Country],
           ["amenity",  Amenity],
           ["place", Place],
           ["review", Review]
          ]

def getClassByName(name):
    '''
        Gets a class by it's singular name (classes[0]) or
        plural name (classes[1])
    '''

    for cls in classes:
        if cls[0] == name or cls[1] == name:
            return cls[2]

    raise ValueError("class not found")
