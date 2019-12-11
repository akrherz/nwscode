#!/usr/bin/env python
# encoding: utf-8
"""
A parser for the *Hydrologic Valid Time Event Code*.

Created by Alexander Ross on 2006-07-15.
Copyright (c) 2006 NOAA's National Weather Service. All rights reserved.
"""

__all__ = ["HvtecError", "Hvtec"]

import re

from nwscode import NwsCode, NwsCodeError
from misc import Bunch, parsevtectime

# Defining HVTEC grammar.
# /nwsli.s.ic.yymmddThhnnZ.yymmddThhnnZ.yymmddThhnnZ.fr/
SITEID = r"[A-Z0-9]{5}"
SEVERITY = r"[N0123U]"
CAUSE = r"[A-Z]{2}"
BEGIN = r"[0-9]{6}T[0-9]{4}Z"
CREST = BEGIN
END = BEGIN
STATUS = r"[A-Z]{2}"
elements = (SITEID, SEVERITY, CAUSE, BEGIN, CREST, END, STATUS)
HVTEC = r"^/(%s)\.(%s)\.(%s)\.(%s)\.(%s)\.(%s)\.(%s)/$" % elements

class HvtecError(NwsCodeError):
    pass

class Hvtec(NwsCode):
    """
    A *Hydrologic Valid Time Event Code* Parser.
    
    Initialize this object with a H-VTEC string. For a full description
    of the H-VTEC format see:
    
        http://www.weather.gov/directives/sym/pd01017003curr.pdf
    
    Attributes:
        
        ``siteid``
            Five character NWS Site Identifier.  For areal flood, flash flood,
            and flood advisory products, encoded as five zeros (00000).
        
        ``floodseverity``
            Identifies the severity of the flooding on rivers and streams
            where point-specific flood warning products are issued.
        
        ``immediatecause``
            Identifies the immediate cause of the flood.
        
        ``floodbegin``
            Represents the actual beginning time of the flooding.
        
        ``floodcrest``
            Represents the actual crest time of the flooding.
        
        ``floodend``
            Represents the actual end time of the flooding.
        
        ``recordstatus``
            Identifies how the flood compares to the flood of record.
    
    Usage Example:
    
    >>> from nwscode.hvtec import HVTEC
    >>> hvtec_string = '/DEMI4.1.ER.030509T2100Z.030510T0300Z.030510T0900Z.NO/'
    >>> hv = HVTEC(hvtec_string)
    >>> hv.floodseverity
    'Minor'
    >>> pv.immediatecause
    'Excessive Rainfall'
    >>> 
    """
    
    pattern = re.compile(HVTEC)
    error = HvtecError
    interpreted = {
        "floodseverity":
            {'N': 'None',
             '0': 'Negligible',
             '1': 'Minor',
             '2': 'Moderate',
             '3': 'Major',
             'U': 'Unknown'},
        "recordstatus" :
            {'OO': 'The flood record status is not applicable.',
             'NO': 'A record flood is not expected.',
             'NR': 'A near record or record flood is expected.',
             'UU': 'There is no period of record to compare to.'},
        "immediatecause":
            {'ER': 'Excessive Rainfall',
             'SM': 'Snowmelt',
             'RS': 'Rain and Snowmelt',
             'DM': 'Dam or Levee Failure',
             'GO': 'Glacier-Dammed Lake Outburst',
             'IJ': 'Ice Jam',
             'IC': 'Rain and/or Snowmelt and/or Ice Jam',
             'FS': 'Upstream Flooding plus Storm Surge',
             'FT': 'Upstream Flooding plus Tidal Effects',
             'ET': 'Elevated Upstream Flow plus Tidal Effects',
             'WT': 'Wind and/or Tidal Effects',
             'DR': 'Upstream Dam or Resevoir Release',
             'MC': 'Other Multiple Causes',
             'OT': 'Other Effects',
             'UU': 'Unknown'}
    }
    
    def _process_matches(self, matches):
        self.code = Bunch(siteid=matches[0],
                        floodseverity=matches[1],
                        immediatecause=matches[2],
                        floodbegin=matches[3],
                        floodcrest=matches[4],
                        floodend=matches[5],
                        recordstatus=matches[6])
        self.siteid = self.code.siteid
        self.floodseverity = self._interpret("floodseverity", matches[1])
        self.immediatecause = self._interpret("immediatecause", matches[2])
        self.floodbegin = parsevtectime(matches[3])
        self.floodcrest = parsevtectime(matches[4])
        self.floodend = parsevtectime(matches[5])
        self.recordstatus = self._interpret("recordstatus", matches[6])
    
