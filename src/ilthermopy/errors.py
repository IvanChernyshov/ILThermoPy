'''Custom errors for the package'''


class ILThermoSearchError(Exception):
    '''Custom error for unsuccessful search queries
    
    Args:
        errors (:obj:`list` of :obj:`str`): error list in search response
    
    Attributes:
        errors (:obj:`list` of :obj:`str`): error list
        message (str): human readable string describing the exception
    
    '''
    
    def __init__(self, errors):
        self.errors = errors
        errors_text = '\n' + ''.join([f'* {e}\n' for e in errors])
        self.message = f'ILThermo search error: {errors_text}'
    
    def __str__(self):
        return self.message


class ILThermoResponseError(Exception):
    '''Custom error for unexpected responses
    
    Args:
        api_name (str): ILThermo's API
        error (str): text of the error
    
    Attributes:
        api_name (str): ILThermo's API
        error (str): text of the error
        message (str): human readable string describing the exception
    
    '''
    
    def __init__(self, api_name: str, error: str):
        self.api_name = api_name
        self.error = error
        self.message = f'{api_name}: {error}'
    
    def __str__(self):
        return self.message


