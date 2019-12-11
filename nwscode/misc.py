#!/usr/bin/env python
# encoding: utf-8
"""
Miscellaneous utilities.

Created by Alexander Ross on 2006-07-20.
Copyright (c) 2006 NOAA's National Weather Service. All rights reserved.
"""

try:
    from datetime import datetime as dt
except ImportError:
    from pydatetime import datetime as dt

from time import strptime, mktime

class Bunch(dict):
    def __init__(self, **kw):
        dict.__init__(self, kw)
        self.__dict__.update(kw)

class RelativeTime(object):
    'The time is relative to time of the product issuance.'
    def __init__(self, day, hour, minute):
        self.day = int(day)
        self.hour = int(hour)
        self.minute = int(minute)

    def offsetfrom(self, root):
        'Returns time relative to root where root is a datetime-like object.'
        if self.day < root.day:
            month = root.month%12 + 1
        if month < root.month:
            year = root.year + 1
        return dt(year, month, self.day, self.hour, self.minute)

    def __cmp__(self, other):
        raise ValueError('It makes no sense to compare RelativeTime objects. '\
                         'Instead, get a datetime from the method '\
                         '`offsetfrom`.')
    def __repr__(self):
        return self.__class__.__name__ + '(%s, %s, %s)' %\
                                              (self.day, self.hour, self.minute)

def parsevtectime(time_string):
    time_pat = '%y%m%dT%H%MZ' # VTEC time code pattern
    if time_string == '000000T0000Z':
        return None
    else:
        return dt.utcfromtimestamp(mktime(strptime(time_string, time_pat)))