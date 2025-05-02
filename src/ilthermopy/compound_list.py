'''Loads pre-readied info on compounds structure

Attributes:
    compounds (Compounds): Compounds object, containing info on compound structures

'''

import sys as _sys
if _sys.version_info < (3, 9):
    import importlib_resources as _importlib_resources
else:
    import importlib.resources as _importlib_resources

from dataclasses import dataclass as _dataclass
import typing as _typing

import pandas as _pd


@_dataclass(repr = False)
class Compounds():
    '''Contains info on compounds' structure'''
    data: _pd.DataFrame
    '''dataframe, containing compound's ID, name, chemical formula (all 
    extracted from ILThermo 2.0), and manually verified SMILES'''
    id2smiles: _typing.Dict[str, str]
    '''dictionary mapping ILThermo's compound ids to SMILES'''
    name2smiles: _typing.Dict[str, str]
    '''dictionary mapping ILThermo's compound names to SMILES'''


def GetSavedCompounds() -> Compounds:
    '''Initializes Compounds object from pre-readied csv-file
    
    Returns:
        Compounds object
    
    '''
    # read data
    pkg = _importlib_resources.files('ilthermopy')
    data_file = pkg / 'data' / 'compounds.csv'
    with _importlib_resources.as_file(data_file) as path:
        data = _pd.read_csv(path)
    # prepare data
    id2smiles = {code: smiles for code, smiles in zip(data.id, data.smiles)}
    name2smiles = {name: smiles for name, smiles in zip(data.name, data.smiles)}
    compounds = Compounds(data, id2smiles, name2smiles)
    
    return compounds


_compounds = GetSavedCompounds()

