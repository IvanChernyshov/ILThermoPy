'''This package is a Python interface for the ILThermo 2.0 database that provides
additional information about the chemical structure of compounds

Attributes:
    compounds (Compound): Compounds object, containing info on compound structures

'''

__version__ = '1.0.0'
__updated__ = 'June 28, 2023'
__license__ = 'MIT'


from ilthermopy.updates import CheckLastUpdate
from ilthermopy.data_structs import PropertyList
from ilthermopy.compound_list import GetCompounds
from ilthermopy.search import ShowPropertyList, Search, GetAllEntries
from ilthermopy.data_structs import GetEntry


