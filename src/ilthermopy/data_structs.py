'''Main classes for quering the ILThermo 2.0 Database'''

#%% Imports

import pandas as _pd
import typing as _typing
from dataclasses import dataclass as _dataclass
from dataclasses import field as _field

import ilthermopy.errors as _err
import ilthermopy.requests as _req
import ilthermopy.misc as _misc

from ilthermopy.compound_list import _compounds as _cmp


#%% Property list

class PropertyList():
    '''Contains info on available physico-chemical properties and their API keys
    
    Attributes:
        properties (dict): two-level organized dictionary, interconnecting property
            types, properties, and their API keys
        key2prop (dict): maps API keys to property names
        prop2key (dict): maps property names to their API keys
    
    '''
    
    def __init__(self):
        self._response = _req.GetPropertyList()
        try:
            self.properties = {item['cls'].strip(): {k.strip(): v.strip() for k, v in zip(item['key'], item['name'])} for item in self._response['plist']}
            self.key2prop = {k: v for name, lst in self.properties.items() for k, v in lst.items()}
            self.prop2key = {v: k for k, v in self.key2prop.items()}
        except (KeyError, AttributeError, TypeError, ValueError):
            raise _err.ILThermoResponseError('Property list (ilprpls) response error', 'Unexpected JSON structure')
        
        return
    
    
    def Show(self) -> None:
        '''Prints list of properties available in ILThermo 2.0 database
        formatted as api_key: property_name'''
        text = []
        for name, props in self.properties.items():
            text += ['\n', f'# {name}\n'] + [f'{k}: {v}\n' for k, v in props.items()]
        print(''.join(text) + '\n')
        
        return


#%% Entry

@_dataclass
class Compound():
    '''Class describing a chemical compound'''
    
    id: str
    '''compound ID'''
    
    name: str
    '''compound name'''
    
    formula: _typing.Optional[str] = _field(default = None, repr = False)
    '''chemical formula of compound'''
    
    smiles: _typing.Optional[str] = _field(default = None)
    '''chemical structure in SMILES format; SMILES is not provided by ILThermo database,
    and is retrieved from manually verified data'''
    
    smiles_error: _typing.Optional[str] = _field(default = None, repr = False)
    '''describes reason why SMILES was not retrieved from pre-readied data;
    None if SMILES was retrieved successfully'''
    
    sample: _typing.Optional[_typing.Dict[str,str]] = _field(default = None, repr = False)
    '''dictionary containing info on compound's source, purity, etc.'''
    
    mw: _typing.Optional[float] = _field(default = None, repr = False)
    '''molar weight, g/mol'''



def ResponseToCompound(response: _typing.Dict) -> Compound:
    '''Transforms entry data API response to the Compound object
    
    Arguments:
        response: dictionary describing compound in entry data API response,
            e.g. r['components'][0]
    
    Returns:
        Compound object
    
    '''
    
    code = response.get('idout', None)
    name = response.get('name', None)
    formula = response.get('formula', None)
    if formula:
        formula = _misc.format_formula(formula)
    smiles = _cmp.id2smiles.get(code, None)
    smiles_error = None
    if not smiles:
        smiles_error = 'No SMILES found for given id, SMILES was retrieved via name'
        smiles = _cmp.name2smiles.get(name, None)
        if not smiles:
            smiles_error = 'No SMILES found for given id and name'
    sample = {k.strip(':'): v for k, v in response.get('sample', None)}
    mw = response.get('mw', None)
    if mw:
        mw = float(mw)
    # initialize
    X = Compound(id = code,
                 name = name,
                 formula = formula,
                 smiles = smiles,
                 smiles_error = smiles_error,
                 sample = sample,
                 mw = mw)
    
    return X



@_dataclass
class Reference():
    '''Class describing a scientific paper'''
    
    full: _typing.Optional[str]
    '''reference text without title'''
    
    title: _typing.Optional[str] = _field(repr = False)
    '''title of the paper'''



@_dataclass
class Entry():
    '''Class describing data entry'''
    
    id: str
    '''data entry ID'''
    
    ref: Reference
    '''source of physico-chemical data'''
    
    property: str
    '''measured property'''
    
    property_type: str
    '''type of measured property'''
    
    phases: _typing.List[str]
    '''list of phases (phase names)'''
    
    components: _typing.List[Compound]
    '''list of chemical components'''
    
    num_components: int = _field(repr = False)
    '''number of chemical components'''
    
    num_phases: int = _field(repr = False)
    '''number of phases'''
    
    num_data_points: int
    '''number of data points'''
    
    expmeth: _typing.Optional[str] = _field(repr = False)
    '''experimental method'''
    
    solvent: _typing.Optional[str] = _field(repr = False)
    '''solvent'''
    
    constraints: _typing.Optional[str] = _field(repr = False)
    '''experimental constraints'''
    
    data: _pd.DataFrame = _field(repr = False)
    '''experimental data in tabular format; columns are formatted as Vi and dVi,
    where Vi is i-th property, and dVi is a corresponding measurement error'''
    
    header: _typing.Dict[str, str] = _field(repr = False)
    '''fullnames of the dataframe's columns'''
    
    footnotes: _typing.Optional[str] = _field(repr = False)
    '''notes to the provided data'''
    
    response: _typing.Dict = _field(repr = False)
    '''data entry API response'''



def ResponseToData(response: _typing.Dict) -> _typing.Tuple[_pd.DataFrame, _typing.Dict]:
    '''Extracts and formats data from data entry API response
    
    Arguments:
        response: data entry API response
    
    Returns:
        dataframe containing experimental data, and dictionary, mapping dataframe's
        column names to fullnames, containing property name, measurement unit,
        and phase name
    
    '''
    # prepare data
    data = [[float(elem) for lst in row for elem in lst] for row in response['data']]
    colnames = []
    for i, elem in enumerate(response['data'][0]):
        if len(elem) == 1:
            addend = [f'V{i+1}']
        elif len(elem) == 2:
            addend = [f'V{i+1}', f'dV{i+1}']
        else:
            raise _err.ILThermoResponseError('Data API (ilset)', f'Number of datapoints per cell must be 1 or 2: {elem}')
        colnames += addend
    data = _pd.DataFrame(data, columns = colnames)
    # set header
    fullnames = []
    for i, column in enumerate(response['dhead']):
        if len(column) == 1:
            fullname = column[0]
        else:
            colname, phase = column
            fullname = f'{colname} => {phase}' if phase else colname
        if len(response['data'][0][i]) == 1:
            fullnames.append(fullname)
        else:
            fullnames += [fullname, 'Error of ' + fullname[0].lower() + fullname[1:]]
    header = {cn: fn for cn, fn in zip(colnames, fullnames)}
    
    return data, header



def ResponseToEntry(code: str, response: _typing.Dict) -> Entry:
    '''Transforms data entry API response to Entry object
    
    Arguments:
        code: data entry ID
        response: data entry API response
    
    Returns:
        Entry object
    
    '''
    ref = Reference(full = response.get('ref', None).get('full', None),
                    title = response.get('ref', None).get('title', None))
    prop = ': '.join([_.strip() for _ in response['title'].split(':')[1:]])
    prop_type = response['title'].split(':')[0].strip()
    phases = response.get('phases', [])
    components = [ResponseToCompound(r) for r in response['components']]
    num_components = len(components)
    num_phases = len(phases)
    expmeth = response.get('expmeth', None)
    solvent = response.get('solvent', None)
    constraints = response.get('constr', [])
    footnotes = response.get('footer', None)
    data, header = ResponseToData(response)
    num_data_points = data.shape[0]
    # build entry
    X = Entry(id = code,
              ref = ref,
              property = prop,
              property_type = prop_type,
              phases = phases,
              components = components,
              num_components = num_components,
              num_phases = num_phases,
              num_data_points = num_data_points,
              expmeth = expmeth,
              solvent = solvent,
              constraints = constraints,
              data = data,
              header = header,
              footnotes = footnotes,
              response = response)
    
    return X


def GetEntry(code: str) -> Entry:
    '''Extracts data entry from ILThermo database
    
    Arguments:
        code: data entry ID
    
    Returns:
        Entry object
    
    '''
    response = _req.GetEntryData(code)
    entry = ResponseToEntry(code, response)
    
    return entry


