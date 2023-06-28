'''Miscellaneous functions'''

import re as _re


def format_formula(formula: str) -> str:
    '''Formats chemical formula from ILThermo format to the alphabetically-ordered one
    
    Arguments:
        formula: HTML-formatted chemical formula in ILThermo 2.0 format
    
    Returns:
        Alphabetically ordered chemical formula
    
    Examples:
        >>> format_formula('C<SUB>4</SUB>H<SUB>10</SUB>O')
        'C4 H10 O'
    
    '''
    formula = formula.replace('<SUB>', '').replace('</SUB>', ' ').strip()
    while _re.search(r'([A-Z])([A-Z])', formula):
        formula = _re.sub(r'([A-Z])([A-Z])', r'\1 \2', formula)
    formula = _re.sub(r'([a-z])([A-Z])', r'\1 \2', formula)
    formula = ' '.join(sorted(formula.split()))
    
    return formula


