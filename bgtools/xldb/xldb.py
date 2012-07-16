'''
Created on Apr 17, 2010

@author: bartmosley
Copyright 2010 BG Research LLC. All rights reserved.

Utility functions:
    xl_to_date
    xlValue

Classes:
    XLSReader
    XLSXReader
    XLdb
    XLOut



'''

import os
import sys

import xlrd
import xlwt

import openpyxl as pyxl

from urllib2 import urlopen, URLError
from datetime import date, timedelta
from tempfile import mkstemp

from .utils import *
from .readers import XLSReader, XLSXReader

class XLdb(object):
    '''
    Container class for loading an Excel Database
    
    Class creates member dictionary with data from the specified 
    spreadsheet.
    
    startrow:       Begin reading at this row (0 indexed), ignore ealier rows
                    
    header:         True--return rows as dict objects, with 'startrow' as keys.
                    False--return rows as list
                    
    sheet:     Name of sheet or 0-indexed sheet number.          
    
    idx_column:     Column to serve as the dict key for qdata.
                    '-1' uses the row number as key.
                    
    numrows:        Number of rows to read.  'None'(default) to read all.
                    
    hash_comments:  True returns 'None' if cell string starts with "#', 
                    ala Bloomberg data errors
                    
    '''
    def __init__(self, filepath, sheet=0,   
                 header=True, idx_column=0, 
                 startrow=0, numrows=None,
                 hash_comments=1,
                 localfile=True):

        self.filepath = filepath
        self.xlsbook = XLSReader(filepath, localfile=localfile)
        self.book = self.xlsbook.book
        
        self.sh = self.xlsbook.sheet(sheet)
        
        sheetdb = self.xlsbook.sheet_as_db(sheet,
                                         header, idx_column,
                                         startrow, numrows)
        
        for attr in ['_key_column', '_hdr', '_qdata']:
            setattr(self, attr, getattr(sheetdb, attr.strip('_'), None))    
        
        self.book.unload_sheet(self.sh.name)
        self.book.release_resources()
    
    @property
    def keys(self):
        return self._key_column
    
    @property
    def hdr(self):
        return self._hdr
    
    @property
    def data(self):
        return self._qdata
    
    
    def get(self, key, default=None):
        if self.qdata:
            return self._qdata.get(key, default)
        else:
            return default
            
    def __getitem__(self, key):
        if self._qdata:
            return self._qdata.get(key, None)
        else:
            return None
    
    def column(self, columnName, reduce=True):
        '''Returns a list for the given column. 
        
        columnName:  The header for the data in qdata.
        reduce:      [default=True], reduces the list to remove Null values
        
        Will retun an empty list if columnName is not a header in the 
        spreadsheet data, not and error.
        
        '''
        colList = [self._qdata[recx].get(columnName, None) 
                   for recx in self._key_column]
                   
        if reduce:
            return filter(lambda x: x is not None, colList)
        else:
            return colList
            

