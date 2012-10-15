'''
Date functions

Author:     Bart Mosley
Created:    6/25/2012

Copyright 2012 BG Research LLC. All rights reserved.

'''

import re
from datetime import date

re_mm = "(?P<M>1[0-2]|0[1-9]|[1-9])"
re_dd = "(?P<D>[0-2][0-9]|3[01]|[1-9])"
re_yyyy = "(?P<Y>[1-9][0-9]{3})"

re_ccyymmdd = re.compile("(?P<Y>[1-9][0-9]{3})(?P<M>[01][0-9])(?P<D>[0-3][0-9])")                                  

re_mm_dd_yyyy = re.compile( "(-|/)".join((re_mm, re_dd, re_yyyy)) )                                         
re_yyyy_mm_dd = re.compile( "(-|/)".join((re_yyyy, re_mm, re_dd)) )


def parse_datetuple(sdate):
    '''Parses ccyymmdd, mm/dd/yyyy or yyyy/mm/dd  
    Returns date tuple: (ccyy, mm, dd) or None if input does not match 
    one of the patterns.
    
    Note: input can be a string or integer (for ccyymmdd pattern).
    
    '''
    sdate = str(sdate)
    
    regex_strings = [re_ccyymmdd, re_mm_dd_yyyy, re_yyyy_mm_dd]
    matches = [re.match(x, sdate) for x in regex_strings]
    
    for m in matches:
        if m:
            return map(int, (m.group('Y'), m.group('M'), m.group('D')))
    
    return None
    
    
def parse_date(sdate):
    '''Parses ccyymmdd, mm/dd/yyyy or yyyy/mm/dd  
    Returns datetime.date or None if input does not match 
    one of the patterns.
    
    Note: input can be a string or integer (for ccyymmdd pattern).

    '''
    tple = parse_datetuple(sdate)
    
    return date(*tple) if tple else None
    
        
            
stddate_re = re.compile("[-//]".join(
        ("(?P<M>[0][1-9]|[1][0-2]|[1-9]{1})", #regex month
         "(?P<D>[0][1-9]|[1-3][0-9]|[1-9]{1})", #regex day
         "(?P<Y>[1-9][0-9]{3}|[0-9][0-9])")   #regex year
         )
    )
                                  
isodate_re = re.compile("[-//]".join(
        ("(?P<Y>[1-9][0-9]{3}|[0-9][0-9])",   #regex year
         "(?P<M>[0][1-9]|[1][0-2]|[1-9]{1})", #regex month
         "(?P<D>[0][1-9]|[1-3][0-9]|[1-9]{1})") #regex day
        )
    )

def int_date(pydate):
    pydate = parse_date(pydate)
    if not pydate:
        return None
    
    return pydate.year * 10000 + pydate.month * 100 + pydate.day
    
    
def ccyymmdd(date_long):
    "returns m, d, y for ccyymmdd date (either integer or string)"
    matched = re.match(re_ccyymmdd, str(date_long))
    if matched is None:
        return None
    
    mdict = matched.groupdict()
    y, m, d = map(int, (mdict['Y'],  mdict['M'], mdict['D']))

    return y, m, d
    
def adjust_year( y, twodigitlag=40):
    """Adjusts a two-digit year to full 4-digit
    
    """
    if y < 100:
        thisyear = date.today().year
        baseyr = (thisyear - twodigitlag) % 100
        cc = thisyear - thisyear % 100
        if y < baseyr:
            y += cc
        else:
            y += cc - 100
    
    return y
            
            
def incr_date(pydate, incr=0):
    try:
        return date.fromordinal(pydate.toordinal()+incr)    
    except:
        return None
        
