'''
This is obsolete given pandas' Reader module

'''
import urllib2
    
from datetime import date
from matplotlib.finance import quotes_historical_yahoo
from bgtools.utils.dates import parse_date

quote_header = ['date', 'open', 'high', 'low', 'close', 'volume']

def dvds_yahoo(ticker, begin, end=None):
    '''     http://ichart.finance.yahoo.com/table.csv?s=AAMBX&a=05&b=20&c=1976&d=09&e=8&f=2012&g=v&ignore=.csv
    '''
    begin, end = map(parse_date, (begin, end))
    if not end:
        end = date.today()
            
    url = ("http://ichart.finance.yahoo.com/table.csv?s={ticker}"+
           "&a={ybegmonth:02d}&b={begin.day}&c={begin.year}" +             
           "&d={yendmonth:02d}&e={end.day}&f={end.year}&g=v&ignore=.csv")
    url_data = dict(ticker=ticker.upper(), begin=begin, end=end,
            ybegmonth=begin.month-1, yendmonth=end.month-1)
    
    url = url.format(**url_data)

    req = urllib2.Request(url)
    try:
        response = urllib2.urlopen(req)

    except urllib2.HTTPError, e:
        print("HTTP Error: {}".format(e.reason))
        return None
    else:
        page_data = response.read().split('\n')
    
    def row_data(x): 
        if len(x) < 2:
            return None
        return parse_date(x[0]), float(x[1])
        
    dvd_data = [row_data(row.split(',')) for row in page_data[1:]
        if row_data(row.split(','))
        ]
    
    return dvd_data

def quotes_yahoo(ticker, begin, end=None, mode='d'):
    '''
    Gets timeseries of stock quotes from yahoo.
    
    mode:  'd' returns {date: (open, high, low, close, volume)}
           'l' list of [(date, open, high, low, close, volume)]
           otherwise numpy structured array
           
    '''
    
    # construct date range for query
    begin, end = map(parse_date, (begin, end))
    if not end: 
        end = date.today()

    date1 = begin.year, begin.month, begin.day
    date2 = end.year, end.month, end.day
    
    # call matplotlib function, asobject=True
    # for structured numpy array
    try:
        quotes = quotes_historical_yahoo(ticker, date1, date2, asobject=True)
    except:
        return None
        
    if mode == 'd':
        vTuple = lambda x: (x['date'], 
                            tuple([x[h] for h in quote_header[1:]]))
    
    elif mode == 'l':
        vTuple = lambda x: tuple([x[h] for h in quote_hdr])
    
    else:
        return quotes
        
    quotes = [vTuple(rec) for rec in quotes]
    
    return dict(quotes) if mode=='d' else quotes
