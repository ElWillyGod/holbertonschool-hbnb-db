
'''
    Defines this folder as a package

    countries csv from: https://github.com/openmundi/world.csv.git
'''

# Exports
import os

if os.environ.get('DATABASE_TYPE') == 'mysql':
    from persistence.data_manager_db import DataManager
    dm = DataManager()
else:
    from persistence.data_manager_file import DataManager
    dm = DataManager("persistence/storage")
