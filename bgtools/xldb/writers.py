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

class XLOut(object):
    '''Creates a workbook object for writing.  
    Defines 'styles', a dict of cell formats, e.g. "date".

    >>> wkb = XLout(filename)
    >>> wkb.write( cell_value, cell_row, cell_column, sheet_index)
    >>> wkb.write( date_value, cell_row2, cell_column2, sheet_index, "date")
    >>> wkb.save()
    
    N.B. 'write' does NOT save (because save can be slow), so you must make sure
    to issue a save before closing, or periodically to avoid losing data.
    
    Utility functions
    =================
        freezepanes:  Allows freezing panes on a specified sheet
        timeseries:   Writes a dictionary {date: value-tuple} to a sheet
        sheet_names:  Property returning list of sheet names
        add_sheet:    Adds a sheet, to the end of the current list of sheets
    
    Most functions allow flexibility in specify sheets, to choose by 
    sheet index or sheet name
    
    '''
    datestyle = xlwt.XFStyle()
    datestyle.num_format_str='MM/DD/YYYY'
    
    pctstyle = xlwt.XFStyle()
    pctstyle.num_format_str="0.000%"
    
    defaultstyle = xlwt.XFStyle()
    
    styles = {"date": datestyle, "pct": pctstyle}
    
    def __init__(self, fname=None, sheets=["Sheet1"], fdir=None,
                       overwrite_ok=False):
        '''
        Creates an excel spreadsheet.
        
        fname:  filename, if not provided a temporary filename is used. filename
                extension will be changed to .xls
        
        sheets: specify what sheets the workbook should have.
                    1. a list of sheet names
                    2. an integer specify how many sheets
                    3. a string specifying the name of a single sheet
                
                Use the add_sheet method to add additional sheets.
                
        fdir:   directory in which to create the file.  If not provided 'fname'
                is taken to be the full path, or if a temporary filename is created
                the file is placed in a default directory
                
           
        '''
        if not fname:
            fd, fpath = mkstemp(dir=fdir, suffix=".xls")
            os.close(fd)
            
        else:
            # make sure file ends with .xls extension
            fname = '.'.join((fname.split('.')[0], "xls"))
            fpath = os.path.join(fdir if fdir else '', fname)
            
        self.filename = fpath
        self.overwrite_ok = overwrite_ok
        
        self.wkb = xlwt.Workbook()                

        # trying to be really flexible in terms of specify sheets
        self.sheet = {}
        try:
            nsheets = len(sheets)
        except:
            try:
                nsheets = int(sheets)
                sheets = ["Sheet%s"%str(n) for n in range(1, nsheets+1)]
            except:
                sheets = [str(sheets)]
                
        for n in range(len(sheets)):
            sheetname = sheets[n]
            self.sheet[n] = self.wkb.add_sheet(sheetname, overwrite_ok)
        
        self.save()
    
    @property
    def sheet_names(self):
        return [self.sheet[n].name.encode() for n in self.sheet]
        
    def get_sheet_name(self, n):
        try:
            return self.sheet[n].name
        
        except:
            return None
            
    def select_sheet(self, sheet=0):
        '''
        Return object for sheet. 'sheet' can be either the index number or
        name of sheet.
        
        '''
        if isinstance(sheet, str):
            try:
                sheet = self.sheet_names.index(sheet)
            
            except:    
                return None
            
        try:
            ws = self.sheet[sheet] 
            return ws
            
        except:
            return None
    
    def add_sheet(self, sheet_name=None):
        'Adds a sheet to the workbook'
        
        if not sheet_name:
            sheet_name = "Sheet%s" % str(len(self.sheets)+1)
        
        self.sheets.append(sheet_name)
        self.sheet.append(self.wkb.add_sheet(sheet_name, overwrite_ok))
        
        return self.sheet[-1]
        
    def write(self, value, row, col, sheet=0, format=None):
        '''
        Writes to specified cell.  DOES NOT SAVE.
        
        Returns None if successfull.  sys.exc_info if not.
        
        '''
        try:
            if type(value) == timedelta:
                #timedelta does not play nicely with xlwt
                value = str(value)
                
            style = self.styles.get(format, self.defaultstyle)
            
            ws = self.select_sheet(sheet)
            ws.write(row, col, value, style)
            
        except:
            print("\nError writing: %s to cell: %s %s %s with format %s" %
                  (value, row, col, sheet, format))
            return sys.exc_info()
        
        return None
        
    def freezepanes(self, row_, col_, sheet=0):
        ws = self.select_sheet(sheet)
        
        ws.set_panes_frozen(True)
        ws.set_remove_splits(True)
        
        ws.set_horz_split_pos(row_+1)
        ws.set_vert_split_pos(col_+1)
        
    def timeseries(self, xdata, sheet=0, hdr=None):
        '''
        xdata:  a dict object, {date_key: value}, where the key is assumed to
                be a datetime.date object.  'value' is either a single value or 
                a tuple (value1, value2, value3)
        
        hdr:    column headings, if not provided ['data', 'value1', ...]
        
        '''
        date_keys = xdata.keys()
        date_keys.sort()
        
        # how will we access data?
        testdata = xdata[date_keys[0]] 
        if hasattr(testdata, "__iter__"):
            get_column_value = lambda colnum: value[colnum-1]
            
        else:
            get_column_value = lambda n: value

        # create header if not provided
        if not hdr:
            hdr = ['date']

            if hasattr(testdata, "__iter__"):
                hdr.extend(['value%s'%str(n) for n in range(1, len(testdata)+1)])
                
            else:
                hdr.append('value1')
        
        # write header row
        for ncol in range(len(hdr)):
            rc = self.write(hdr[ncol], 0, ncol, sheet)
            if rc:
                print("\nXLOut.timeseries problem writing header:\n%s\n" % rc)
                print("Sheet %s, row %s, column %\n" % (sheet, 0, ncol))
                return rc
                
        # write data rows
        for nrow, dt in enumerate(date_keys, start=1):
            self.write(dt, nrow, 0, sheet, format='date')
            
            value = xdata[dt]
            for ncol in range(1, len(hdr)):
                rc = self.write(get_column_value(ncol), nrow, ncol, sheet)   
                if rc:
                    print("\nXLOut.timeseries problem writing data:\n%s\n" % rc)
                    print("Sheet %s, row %s, column %\n" % (sheet, nrow, ncol))
                    return rc
                    
    def save(self):
        self.wkb.save(self.filename)

def timeseries_toXLS(xdata, fname=None, fdir=None, hdr=None):
    '''
    Writes Timeseries data to a spreadsheet.
    
    xdata:  a dict object, {date_key: value}, where the key is assumed to
            be a datetime.date object.  'value' is either a single value or 
            a tuple (value1, value2, value3)
    
    fname:  filename, if not provided a temporary filename is used. filename
            extension will be changed to .xls
    
    fdir:   directory in which to create the file.  If not provided 'fname'
            is taken to be the full path, or if a temporary filename is created
            the file is placed in a default directory
    
    hdr:    column headings, if not provided ['data', 'value1', ...]
    '''

    # use tempfile.mkstemp to create file name if not provided
    if not fname:
        fd, fpath = mkstemp(dir=fdir, suffix=".xls")
        os.close(fd)
    else:
        # make sure file ends with .xls extension
        fname = '.'.join((fname.split('.')[0], "xls"))
        fpath = os.path.join(fdir if fdir else '', fname)
        
    wkb = XLOut(fpath)
    
    date_keys = xdata.keys()
    date_keys.sort()
    
    # create header if not provided
    if not hdr:
        testdata = xdata[date_keys[0]]        
        hdr = ['date']
        try:
            hdr.extend(['value'+str(n) for n in range(1, len(testdata))+1])
            
        except:
            hdr.append('value1')
    
    # write header row
    for ncol in range(len(hdr)):
        wkb.write(hdr[ncol], 0, ncol, 0)
    
    # write data rows
    for nrow, dt in enumerate(date_keys, start=1):
        wkb.write(dt, nrow, 0, 0, format='date')
        
        for ncol in range(1, len(hdr)):
            value = xdata[dt]
            wkb.write(value, nrow, ncol, format=hdr[ncol][1])
            
    wkb.save()

    return fpath
