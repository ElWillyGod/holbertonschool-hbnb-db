
'''
    Defines this folder as a package

    countries csv from: https://github.com/openmundi/world.csv.git
'''

from persistence.data_manager import DataManager
from persistence.model import model_amenity

DM = DataManager("persistence/storage")
