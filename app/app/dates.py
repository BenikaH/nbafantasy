# dates.py
# common date routines

import datetime
import logging
import re


def add_days_to_datestr(datestr, n):
    '''
    Add n days to a datestring

    Args:
        datestr (str): 
        n (int): 

    Returns:
        str
        
    '''
    fmt = format_type(datestr)
    if not fmt:
        raise ValueError('invalid datestring format: {}'.format(datestr))
    if not isinstance(n, int):
        raise ValueError('n={} must be an integer'.format(n))
    d = strtodate(datestr)
    d2 = d + datetime.timedelta(days=n)
    return datetime.datetime.strftime(d2, format_type(datestr))


def convert_format(d, site):
    '''
    Converts string from one date format to another

    Args:
        d: datestring
        site: 'nba', 'fl', 'std', etc.

    Returns:
        Datestring in new format
    '''
    fmt = format_type(d)
    newfmt = site_format(site)
    if fmt and newfmt:
        try:
            dt = datetime.datetime.strptime(d, fmt)
            return datetime.datetime.strftime(dt, newfmt)
        except:
            return None
    else:
        return None

def date_before(d1, d2, fmt='%Y-%m-%d'):
    '''
    Determines if first date is before the second date
    
    Args:
        d1: 
        d2: 
        fmt: 

    Returns:
        bool: True is date is earlier, false if not
        
    '''
    dt1 = datetime.datetime.strftime(d1, fmt)
    dt2 = datetime.datetime.strftime(d2, fmt)


def date_list(d1, d2, delta=None):
    '''
    Takes two datetime objects or datestrings and returns a list of datetime objects

    Args:
        d1: more recent datetime object or string
        d2: less recent datetime object or string

    Returns:
        dates (list): list of datetime objects
        
    Examples:
        for d in date_list('10_09_2015', '10_04_2015'):
            print datetime.strftime(d, '%m_%d_%Y')
    '''
    if isinstance(d1, str):
        try:
            d1 = strtodate(d1)
        except:
            logging.error('{0} is not in %m_%d_%Y format'.format(d1))
    if isinstance(d2, str):
        try:
            d2 = strtodate(d2)
        except:
            logging.error('{0} is not in %m_%d_%Y format'.format(d1))

    if delta:
        dlist = []
        while d2 <= d1:
            dlist.append(d2)
            d2 += + datetime.timedelta(days=delta)
        return dlist
    else:
        season = d1 - d2
        return [d1 - datetime.timedelta(days=x) for x in range(0, season.days+1)]


def datetostr(d, fmt):
    '''
    Converts datetime object to formats used by different sites

    Args:
        d: DateTime object
        fmt: str, such as 'nba' or 'fl'

    Returns:
        datestr in specified format
    '''
    try:
        return datetime.datetime.strftime(d, site_format(fmt))
    except:
        return ''

def format_type(datestr):
    '''
    Uses regular expressions to determine format of datestring

    Args:
        d (str): date string in a variety of different formats

    Returns:
        fmt (str): format string for date

    '''

    if re.match(r'\d{1,2}_\d{1,2}_\d{4}', datestr):
        return site_format('fl')

    elif re.match(r'\d{4}-\d{2}-\d{2}', datestr):
        return site_format('nba')

    elif re.match(r'\d{1,2}-\d{1,2}-\d{4}', datestr):
        return site_format('std')

    elif re.match(r'\d{8}', datestr):
        return site_format('db')

    else:
        return None


def site_format(site):
    '''
    Stores date formats used by different sites
    '''
    fmt = {
        'std': '%m-%d-%Y',
        'fl': '%m_%d_%Y',
        'nba': '%Y-%m-%d',
        'db': '%Y%m%d'
    }
    return fmt.get(site, None)


def strtodate(d):
    '''
    Converts date formats used by different sites
    '''
    return datetime.datetime.strptime(d, format_type(d))


def subtract_datestr(d1, d2):
    '''
    Subtracts d2 from d1
    Args:
        d1: datestr
        d2: datestr

    Returns:
        int
    '''
    try:
        delta = strtodate(d1) - strtodate(d2)
    except:
        delta = d1 - d2
    return delta.days


def today(fmt='nba'):
    '''
    Datestring for today's date

    Args:
        fmt: str, code like 'nba'

    Returns:
        datestr
    '''
    fmt = site_format(fmt)
    if not fmt:
        raise ValueError('invalid date format')
    return datetime.datetime.strftime(datetime.datetime.today(), fmt)


def yesterday(fmt='nba'):
    '''
    Datestring for yesterday's date

    Args:
        fmt: str, code like 'nba'

    Returns:
        datestr
    '''
    fmt = site_format(fmt)
    if not fmt:
        raise ValueError('invalid date format')
    return datetime.datetime.strftime(datetime.datetime.today() - datetime.timedelta(1), fmt)
