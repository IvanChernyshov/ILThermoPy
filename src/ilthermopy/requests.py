'''Request wrappers for ILThermo APIs

Attributes:
    BASE_URL   (str): base URL of the ILThermo 2.0 database
    PROPS_URL  (str): relative URL for the property list API
    SEARCH_URL (str): relative URL for the search API
    DATA_URL   (str): relative URL for loading entrie's data
    IMAGE_URL  (str): relative URL for compound's image API

'''

import requests as _requests
import typing as _typing
try:
    from typing import Literal as _Literal
except ImportError:
    from typing_extensions import Literal as _Literal


# API URLs
BASE_URL   = 'https://ilthermo.boulder.nist.gov/'
PROPS_URL  = f'{BASE_URL}/ILT2/ilprpls'
SEARCH_URL = f'{BASE_URL}/ILT2/ilsearch'
DATA_URL   = f'{BASE_URL}/ILT2/ilset'
IMAGE_URL = f'{BASE_URL}/ILT2/ilimage'


def GetHomepage() -> str:
    '''Returns HTML of the ILThermo's homepage
    
    Returns:
        HTML-formatted ILThermo homepage (JS functionality disabled)
    
    '''
    r = _requests.get(BASE_URL)
    r.raise_for_status()
    
    return r.text


def GetPropertyList() -> dict:
    '''Extracts available ILThermo properties and their API keys
    
    Returns:
        dictionary containing two-level structured info on
        currently available physchemical properties and their API keys
    
    '''
    r = _requests.get(PROPS_URL)
    r.raise_for_status()
    
    return r.json()


def GetEntries(compound: _typing.Optional[str] = None,
               n_compounds: _Literal[None,1,2,3] = None,
               prop_key: _typing.Optional[str] = None,
               year: _typing.Optional[int] = None,
               author: _typing.Optional[str] = None,
               keywords: _typing.Optional[str] = None) -> dict:
    '''Wrapper for database search request
    
    Arguments:
        compound: chemical formula, CAS registry number, or name (part or full)
        n_compounds: number of mixture compounds
        prop_key: key of physico-chemical property (view available via GetPropertyList)
        year: publication year
        author: author's last name
        keywords: keywords presumably specified in paper's title
    
    Returns:
        dictionary containing ILThermo search response
    
    '''
    params = {'cmp' : compound,
              'ncmp': n_compounds,
              'year': year,
              'auth': author,
              'keyw': keywords,
              'prp' : prop_key}
    params = {key: '' if val is None else val for key, val in params.items()} # to get the same url as in the website
    r = _requests.get(SEARCH_URL, params)
    r.raise_for_status()
    
    return r.json()


def GetEntryData(setid: str) -> dict:
    '''Wrapper for loading of data entry
    
    Arguments:
        setid: entry ID
    
    Returns:
        dictionary containing info on data entry, including reference, compounds,
        physico-chemical data, etc.
    
    '''
    
    r = _requests.get(DATA_URL, {'set': setid})
    r.raise_for_status()
    
    return r.json()


def GetCompoundImage(idout: str) -> bytes:
    '''Wrapper for loading of compound's image
    
    Arguments:
        idout: compound ID
    
    Returns:
        bytes-formatted PNG image
    
    '''
    
    r = _requests.get(IMAGE_URL, {'key': idout})
    r.raise_for_status()
    
    return r.content


