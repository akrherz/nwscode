#!/usr/bin/env python
# encoding: utf-8
"""
A parser for the *WMO Abbreviated Header*.

Created by Alexander Ross on 2006-07-20.
Copyright (c) 2006 NOAA's National Weather Service. All rights reserved.
"""

__all__ = ["WmoError", "WmoHeader", "WmoFile"]

import re
from misc import Bunch, RelativeTime
from nwscode import NwsCode, NwsCodeError

_designator = r"[A-Z]{4}[0-9]{2}"
_station = r"[A-Z0-9]{4}"
_issuance = r"[0-9]{6}"
_addendum = r"[A-Z]{3}"
_wmoheader = "^(%s) (%s) (%s)(?: (%s))?$" \
                                % (_designator, _station, _issuance, _addendum)
_wmofile = "^(%s)(%s)$" % (_designator, _station)

class WmoError(NwsCodeError):
    pass

class WmoHeader(NwsCode):
    """
    A *World Meteorological Organization Abbreviated Header* parser.
    
    For a full description of the WMO Header format see WMO Manual's 306
    and 386.  The National Weather Service has made much of this information
    available at the following address:
    
        http://www.weather.gov/tg/headef.html
    
    Attributes:
    
        ``designator``
            Designator for the contents of the bulletin.
    
        ``station``
            The identification of the processing center that generated
            the bulletin.
    
        ``issuance``
            The product issuance time.
    
        ``addendum``
            The optional BBB group.
    """

    pattern = re.compile(_wmoheader)
    error = WmoError

    def _process_matches(self, matches):
        self.code = Bunch(designator=matches[0],
                          station=matches[1],
                          expiration=matches[2])
        # could write a more detailed processor for the designator.
        self.designator = matches[0]
        self.station = matches[1]
        time_string = matches[2]
        day, hour, minute = time_string[:2], time_string[2:4], time_string[4:]
        self.issuance = RelativeTime(day, hour, minute)
        if len(matches) == 4:
            self.addendum = matches[3]
    

class WmoFile(NwsCode):
    # this class needs a new name, but I can't get on the internet atm
    # to find out what that name should be.
    """
    A *World Meteorological Organization* file name parser.
    
    For a full description of the WMO Header format see WMO Manual's 306
    and 386.  The National Weather Service has made much of this information
    available at the following address:
    
        http://www.weather.gov/tg/headef.html
    
    Attributes:
    
        ``designator``
            Designator for the contents of the bulletin.
    
        ``station``
            The identification of the processing center that generated
            the bulletin.
    """

    pattern = re.compile(_wmofile)
    error = WmoError

    def _process_matches(self, matches):
        self.code = Bunch(designator=matches[0],
                          station=matches[1])
        # could write a more detailed processor for the designator.
        self.designator = matches[0]
        self.station = matches[1]
    
