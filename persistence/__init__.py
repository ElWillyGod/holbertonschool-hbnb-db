
'''
    Defines this folder as a package

    countries csv from: https://github.com/openmundi/world.csv.git
'''

# Exports
from persistence.data_manager import DataManager

dm = DataManager("persistence/storage")
