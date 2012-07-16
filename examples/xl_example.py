'''
xl_example.py

Reading data to and from .xls spreadsheets

@author: bartmosley
Copyright 2010 BG Research LLC. All rights reserved.

'''

import random
import math

from datetime import date

from bgtools.xldb import XLdb, XLOut, timeseries_toXLS

if __name__ == "__main__":
    
    #create a sample time series
    x = [(date(1980,9,7), 100.0), ]
    for n in range(1, 100):
        x.append((  date.fromordinal(x[n-1][0].toordinal()+1),
                    x[n-1][1] * (1. + random.gauss(0., 1.) * .0070))
                    )
    
    # Create a spreadsheet from the time series
    # if no filename/path is specified, creates a temporary file
    fn = timeseries_toXLS(dict(x))
    print("File path: %s" % fn)
    
    # Read spreadsheet into a data object
    dbx = XLdb(fn)
    print("\nNumber of rows: %s\nHeader: %s" %(len(dbx.keys), dbx.hdr))
    dt0 = dbx.keys[0]
    print("\nFirst row:\n> %s, %s" % (dt0, dbx[dt0][dbx.hdr[1]]))
            
    
    
