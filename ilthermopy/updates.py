'''Checks if ilthermopy package is up-to-date with ILThermo 2.0 database'''

import re as _re
from datetime import datetime as _datetime

from ilthermopy import __updated__
import ilthermopy.errors as _err
import ilthermopy.requests as _req


def CheckLastUpdate() -> None:
    '''Prints date of the last ILThermo 2.0 update'''
    # get update date from homepage
    html = _req.GetHomepage()
    match = _re.search('Updated on ([a-zA-Z]+ +\d+, +\d+)', html)
    if match is None:
        raise _err.ILThermoResponseError('Homepage', 'cannot extract update date')
    # compare dates
    try:
        db_updated = _datetime.strptime(match.group(1), '%B %d, %Y')
    except ValueError:
        raise _err.ILThermoResponseError('Homepage', f'cannot parse extracted update date: "{match.group(1)}"')
    lib_updated = _datetime.strptime(__updated__, '%B %d, %Y')
    # message
    print(f'ILThermo 2.0 database was last updated on {db_updated.strftime("%B %d, %Y")}')
    print(f'ilthermopy package was last updated on {lib_updated.strftime("%B %d, %Y")}\n')
    if lib_updated >= db_updated:
        print('ilthermopy package is up-to-date')
    else:
        print('ilthermopy package is oudated, be careful when using SMILES-related features')
    
    return


