
'''
    Defines this folder as a package

    countries csv from: https://github.com/openmundi/world.csv.git
'''

from persistence.data_manager import db, DataManager


DM = DataManager("persistence/storage")
