'''Search-related functions'''

import typing as _typing
try:
    from typing import Literal as _Literal
except ImportError:
    from typing_extensions import Literal as _Literal

import pandas as _pd

import ilthermopy.errors as _err
import ilthermopy.requests as _req
import ilthermopy.data_structs as _ds

from ilthermopy.compound_list import _compounds as _cmp


def ShowPropertyList() -> None:
    '''Prints list of properties available in ILThermo 2.0 database'''
    _ds.PropertyList().Show()
    
    return


def _SearchItemToRow(r: _typing.List) -> _typing.Dict:
    '''Transforms row in ILThermo search response to the dictionary formatted 
    for the dataframe containing search results'''
    # basic info
    row = {'id': r[0],
           'reference': r[1],
           'property': r[2],
           'phases': r[3],
           'num_phases': r[3].count(';') + 1,
           'num_components': len(r) - 8,
           'num_data_points': int(r[7])}
    # compounds
    for i, j in enumerate(range(4, 7)):
        code, name = (r[j], r[j+4]) if r[j] is not None else (None, None)
        row[f'cmp{i+1}'] = name
        row[f'cmp{i+1}_id'] = code
        smiles = _cmp.id2smiles.get(code, None)
        if not smiles:
            smiles = _cmp.name2smiles.get(name, None)
        row[f'cmp{i+1}_smiles'] = smiles
    
    return row


def Search(compound: _typing.Optional[str] = None,
           n_compounds: _Literal[None,1,2,3] = None,
           prop: _typing.Optional[str] = None,
           prop_key: _typing.Optional[str] = None,
           year: _typing.Optional[int] = None,
           author: _typing.Optional[str] = None,
           keywords: _typing.Optional[str] = None) -> _pd.DataFrame:
    '''Runs ILThermo search and returns results as a dataframe
    
    Arguments:
        compound: chemical formula, CAS registry number, or name (part or full)
        n_compounds: number of mixture compounds
        prop: name of physico-chemical property, only used if prop_key is not specified
        prop_key: key of physico-chemical property (view available via GetPropertyList)
        year: publication year
        author: author's last name
        keywords: keywords presumably specified in paper's title
    
    Returns:
        dataframe containing main info on found entries
    
    '''
    # get property key
    if not prop_key and prop:
        plist = _ds.PropertyList()
        prop_key = plist.prop2key.get(prop, None)
        if prop_key is None:
            raise ValueError(f'Unknown property: {prop}\nCheck available properties via the ilt.ShowPropertyList function')
    # run search API
    data = _req.GetEntries(compound = compound,
                           n_compounds = n_compounds,
                           prop_key = prop_key,
                           year = year,
                           author = author,
                           keywords = keywords)
    # process returned errors
    errors = data.get('errors', [])
    if errors:
        raise _err.ILThermoSearchError(errors)
    # transform to table
    try:
        rows = [_SearchItemToRow(r) for r in data['res']]
    except (KeyError, IndexError, ValueError, TypeError):
        raise _err.ILThermoResponseError('Search API', 'Unexpected JSON structure')
    df = _pd.DataFrame(rows)
    
    return df


def GetAllEntries() -> _pd.DataFrame:
    '''Returns main info on all available ILThermo entries
    
    Returns:
        dataframe containing all currently available entries
    
    '''
    df = _pd.concat([Search(n_compounds = i) for i in (1,2,3)],
                    ignore_index = True)
    
    return df


