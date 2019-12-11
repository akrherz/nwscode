#!/usr/bin/env python
# encoding: utf-8
"""
A parser for the *Primary Valid Time Event Code*.

Created by Alexander Ross on 2006-07-15.
Copyright (c) 2006 NOAA's National Weather Service. All rights reserved.
"""

__all__ = ["PvtecError", "Pvtec"]

import re
from nwscode import NwsCode, NwsCodeError
from misc import Bunch, parsevtectime

# PVTEC Grammar.
FIXEDIDENT = r"[OTEX]"
ACTION = r"[A-Z]{3}"
OFFICEIDENT = r"[A-Z]{4}"
PHENOMENA = r"[A-Z]{2}"
SIGNIFICANCE = r"[WAYSFON]"
ETN = r"[0-9]{4}"
EVENTBEGIN = r"[0-9]{6}T[0-9]{4}Z"
EVENTEND = EVENTBEGIN
elements = (FIXEDIDENT, ACTION, OFFICEIDENT, PHENOMENA,
            SIGNIFICANCE, ETN, EVENTBEGIN, EVENTEND)
PVTEC = r"^/(%s)\.(%s)\.(%s)\.(%s)\.(%s)\.(%s)\.(%s)\-(%s)/$" % elements

class PvtecError(NwsCodeError):
    pass

class Pvtec(NwsCode):
    """
    A ``Primary Valid Time Event NwsCode`` parser.
    
    For a full description of the P-VTEC format see the National Weather
    Service's VTEC Directive:
        
        http://www.nws.noaa.gov/directives/sym/pd01017003curr.pdf
    
    Attributes:
        
        ``fixedid``
            The Fixed Identifier. Identifies the following product and VTEC
            code string types.
        
        ``action``
            Identifies the action in the product issuance.
        
        ``officeid``
            The standard four-letter identifier indicating the NWS office
            with the primary responsibility for the affected area.
        
        ``phenomena``
            Identifies the type of weather, flood, marine, fire weather,
            etc., occurrence (e.g., freezing rain, river flood, gale, red
            flag), or non-weather occurrence (e.g., ashfall).
        
        ``significance``
            Identifies the level of importance (e.g., watch, warning,
            advisory, etc.) of the weather or non-weather occurrence.
        
        ``etn``
            The ETN is a four-digit number assigned to keep track of how an
            event is addressed by various VTEC actions and/or products issued
            over the lifetime of the event.
        
        ``eventbegin``
            Start of the valid time span for the event.
        
        ``eventend``
            End of the valid time span for the event.
    
    Usage Example:
    
    >>> from nwscode.pvtec import PVTEC
    >>> pvtec_string = '/X.EXT.PAFG.FG.Y.0002.000000T0000Z-060127T2100Z/'
    >>> pv = PVTEC(pvtec_string)
    >>> pv.action
    'Extended in time'
    >>> pv.significance
    'Advisory'
    >>>
    """
    
    pattern = re.compile(PVTEC, re.M)
    error = PvtecError
    interpreted = {
        "action":
            {'NEW': 'New',
             'CON': 'Continued',
             'EXT': 'Extended in time',
             'EXA': 'Extended in area',
             'UPG': 'Upgraded',
             'CAN': 'Cancelled',
             'EXP': 'Expired',
             'COR': 'Correction',
             'ROU': 'Routine'},
        "fixedid":
            {'O': 'Operational Product',
             'T': 'Test Product',
             'E': 'Experimental Product',
             'X': 'Experimental VTEC in an Operational Product'},
        "phenomena":
            {'AF': 'Ashfall',
             'AS': 'Air Stagnation',
             'BS': 'Blowing Snow',
             'BW': 'Brisk Wind',
             'BZ': 'Blizzard',
             'CF': 'Coastal Flood',
             'DS': 'Dust Storm',
             'DU': 'Blowing Dust',
             'EC': 'Extreme Cold',
             'EH': 'Excessive Heat',
             'FA': 'Areal Flood',
             'FF': 'Flash Flood',
             'FG': 'Dense Fog',
             'FL': 'Flood',
             'FR': 'Frost',
             'FW': 'Fire Weather',
             'FZ': 'Freeze',
             'GL': 'Gale',
             'HF': 'Hurricane Force Wind',
             'HI': 'Inland Hurricane',
             'HS': 'Heavy Snow',
             'HT': 'Heat',
             'HU': 'Hurricane',
             'HW': 'High Wind',
             'HY': 'Hydrologic',
             'HZ': 'Hard Freeze',
             'IP': 'Sleet',
             'IS': 'Ice Storm',
             'LB': 'Lake Effect Snow and Blowing Snow',
             'LE': 'Lake Effect Snow',
             'LO': 'Low Water',
             'LS': 'Lakeshore Flood',
             'LW': 'Lake Wind',
             'MA': 'Marine',
             'RB': 'Small Craft for Rough Bar',
             'SB': 'Snow and Blowing Snow',
             'SC': 'Small Craft',
             'SE': 'Hazardous Seas',
             'SI': 'Small Craft for Winds',
             'SM': 'Dense Smoke',
             'SN': 'Snow',
             'SR': 'Storm',
             'SU': 'High Surf',
             'SV': 'Severe Thunderstorm',
             'SW': 'Small Craft for Hazardous Seas',
             'TI': 'Inland Tropical Storm',
             'TO': 'Tornado',
             'TR': 'Tropical Storm',
             'TS': 'Tsunami',
             'TY': 'Typhoon',
             'UP': 'Ice Accretion',
             'WC': 'Wind Chill',
             'WI': 'Wind',
             'WS': 'Winter Storm',
             'WW': 'Winter Weather',
             'ZF': 'Freezing Fog',
             'ZR': 'Freezing Rain'},
        "significance":
            {'W': 'Warning',
             'A': 'Watch',
             'Y': 'Advisory',
             'S': 'Statement',
             'F': 'Forecast',
             'O': 'Outlook',
             'N': 'Synopsis'}
    }

    def _process_matches(self, matches):
        self.code = Bunch(fixedid=matches[0],
                        action=matches[1],
                        officeid=matches[2],
                        phenomena=matches[3],
                        significance=matches[4],
                        etn=matches[5],
                        eventbegin=matches[6],
                        eventend=matches[7])
        self.fixedid = self._interpret("fixedid", matches[0])
        self.action = self._interpret("action", matches[1])
        self.officeid = matches[2]
        self.phenomena = self._interpret("phenomena", matches[3])
        self.significance = self._interpret("significance", matches[4])
        self.etn = int(matches[5])
        self.eventbegin = parsevtectime(matches[6])
        self.eventend = parsevtectime(matches[7])