__all__ = ['get_xlvalue', 'xl_to_date', 'xlValue']

from datetime import date

import xlrd

def get_xlvalue(h_):
    '''Returns contents of cell, stripping plain-text out of unicode.
    
    '''
    if hasattr(h_.value, "encode"):
        return h_.value.encode()
    else:
        return h_.value
            
def xl_to_date(xdate, _datemode = 1):
    yyyy, mm, dd, h, m, s =xlrd.xldate_as_tuple(xdate.value, _datemode)
    return date(yyyy, mm, dd)

def xlValue(x, datemode=1, hash_comments=1, strip_text=1):
    try:
        if(x.ctype == xlrd.XL_CELL_EMPTY or
           x.ctype == xlrd.XL_CELL_BLANK or
           x.ctype == xlrd.XL_CELL_ERROR):
            return ""
            
        if(x.ctype == xlrd.XL_CELL_TEXT):
            t = x.value.encode()
            if hash_comments and t[0] == '#':
                return None
            else:
                return t.strip() if strip_text else t
                
        if(x.ctype == xlrd.XL_CELL_DATE):
            yyyy, mm, dd, h, m, s = xlrd.xldate_as_tuple(x.value,
                                                         datemode)
            return date(yyyy, mm, dd)
            
        else:
            # that leaves XL_CELL_NUMBER and XL_CELL_BOOLEAN
            return x.value
            
    except:
        return None 