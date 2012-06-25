'''
Date functions

Author:     Bart Mosley
Created:    6/25/2012

Copyright 2012 BG Research LLC. All rights reserved.

'''

import re
from datetime import date
            
stddate_re = re.compile("[-//]".join(
        ("(?P<Y>[0][1-9]|[1][0-2]|[1-9]{1})", #regex month
         "(?P<M>[0][1-9]|[1-3][0-9]|[1-9]{1})", #regex day
         "(?P<D>[1-9][0-9]{3}|[0-9][0-9])")   #regex year
         )
    )
                                  
isodate_re = re.compile("[-//]".join(
        ("(?P<Y>[1-9][0-9]{3}|[0-9][0-9])",   #regex year
         "(?P<M>[0][1-9]|[1][0-2]|[1-9]{1})", #regex month
         "(?P<D>[0][1-9]|[1-3][0-9]|[1-9]{1})") #regex day
        )
    )

longdate_re = re.compile("(?P<Y>[1-9][0-9]{3})(?P<M>[0-1][0-9])(?P<D>[0-3][0-9])")                                  

def ccyymmdd(date_long):
    "returns m, d, y for ccyymmdd date (either integer or string)"
    matched = re.match(longdate_re, str(date_long))
    if matched is None:
        return None
    
    y, m, d = map(int, (matched.group('Y'), m.group('M'), m.group('D')))

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
            
def strdate_tuple(sdate, twodigitlag=40):
    '''
    Given a date in string format return year, month, day tuple
    - year is in ccyy format
    - date string may use either "-" or "/" separators
    - date string may be mm/dd/ccyy, mm/dd/yy, ccyy-mm-dd, yy-mm-dd 
      or ccyymmdd formats
    - an integer ccyymmdd also works (but not yymmdd).
    
    '''
    sdate = str(sdate) # in case int is given
    
    matched = [re.match(stddate_re, sdate),
               re.match(isodate_re, sdate),
               re.match(longdate_re, sdate)]
    
    for x in matched:
        if x:
            y, m, d = map(int, (matched.group('Y'), m.group('M'), m.group('D')))
            return adjust_year(y, twodigitlag), m, d
    
    return None

def str_to_date(sdate, twodigitlag=40):
    dt_tuple = strdate_tuple(sdate, twodigitlag)
    
    return date(*dt_tuple) if dt_tuple else None