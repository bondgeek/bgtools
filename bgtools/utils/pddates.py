# -*- coding: utf-8 -*-
"""
Created on Tue Jan 08 18:12:16 2013

@author: Bart
"""
import pandas as pd

from datetime import date, datetime
from bgtools.utils.dates import parse_date
from pandas.tseries.offsets import (
    MonthEnd, YearEnd, BDay, BMonthEnd, BQuarterEnd, BYearEnd
    )

# date handling tools
def pdparse_date(ndate):
    xdt = parse_date(ndate)
    return pd.Timestamp(xdt)
    
def nDayOfWeek(pydate, n=-1, isoweekday=3):
    '''
    isoweekday: Monday=1, Tuesday=2, Wednesday=3, Thursday=4, Friday-5
    Defaults to previous 
    
    '''
    pydate = parse_date(pydate)
    
    return pd.DateOffset(pydate, days=isoweekday-pydate.isoweekday())

def nOffset(pydate, n=-1, offsetClass=BDay):
    '''
    Generate offset python datetime.date based on pandas offset class
    offsetClass:  BDay (default), MonthEnd, or YearEnd
    
    '''
    pydate = parse_date(pydate)
    
    offSet = offsetClass(n)
    return pd.Timestamp((datetime.fromordinal(pydate.toordinal()) + offSet))
    
    
def offset_index(df, n=-1, offsetClass=BDay, fOffset=nOffset):
    '''
    list of dates offset by
    Day of Week:  offset_index(df, -1, 3, nDayOfWeek)
    Pandas offset class:  offset_index(df, -1, MonthEnd, nOffset)
    
    '''
    dtidx = df.index
    
    dtoffset = [(dt, fOffset(dt, n, offsetClass)) for dt in dtidx]
    return [(dt, dt0) for dt, dt0 in dtoffset if not pd.isnull(dt0)]


def df_index_bdays(tseries, freq='M'):
    '''
    Create a list of dates from a pandas timeseries, such that the new list
    contains business days of the specified frequency.
    '''
    
    start_dt, end_dt = tseries.index.min(), tseries.index.max()
    
    x_dates = pd.date_range(start=start_dt, end=end_dt, freq=freq)
    
    me = lambda x: BDay().rollback(pd.Timestamp(x))
    
    return pd.Series([me(dt) for dt in x_dates])
    

