'''
Date functions

Author:     Bart Mosley
Created:    6/25/2012

Copyright 2012 BG Research LLC. All rights reserved.

'''

import re
from datetime import date
            
stddate_re = re.compile("[-//]".join(("([0][1-9]|[1][0-2]|[1-9]{1})", #regex month
                                   "([0][1-9]|[1-3][0-9]|[1-9]{1})", #regex day
                                   "([1-9][0-9]{3}|[0-9][0-9])")   #regex year
                                  ))
                                  
isodate_re = re.compile("[-//]".join(("([1-9][0-9]{3}|[0-9][0-9])",   #regex year
                                   "([0][1-9]|[1][0-2]|[1-9]{1})", #regex month
                                   "([0][1-9]|[1-3][0-9]|[1-9]{1})") #regex day
                                  ))

longdate_re = re.compile("(?P<Y>[1-9][0-9]{3})(?P<M>[0-1][0-9])(?P<D>[0-3][0-9])")                                  

def ccyymmdd(date_long):
    "returns m, d, y for ccyymmdd date (either integer or string)"
    m = re.match(longdate_re, str(date_long))
    if m is None:
        return None
    
    return map(int, (m.group('M'), m.group('D'), m.group('Y')))
    
def strDateTuple(sdate, twodigitlag=40):
    '''
    Given a date in string format return month, day, year tuple
    - year is in ccyy format
    - date string may use either "-" or "/" separators
    - date string may be mm/dd/ccyy, mm/dd/yy, ccyy-mm-dd, yy-mm-dd 
      or ccyymmdd formats
    - an integer ccyymmdd also works (but not yymmdd).
    '''
    sdate = str(sdate) # incase int is given
    stdgrp = re.match(stddate_re, sdate)
    isogrp = re.match(isodate_re, sdate)
    if stdgrp:
        m, d, y = map(int, stdgrp.groups())
    elif isogrp:
        y, m, d = map(int, isogrp.groups())
    else:
        return ccyymmdd(sdate)
        
    if y < 100:
        thisyear = date.today().year
        baseyr = (thisyear - twodigitlag) % 100
        cc = thisyear - thisyear % 100
        if y < baseyr:
            y += cc
        else:
            y += cc - 100
            
    return m, d, y


                