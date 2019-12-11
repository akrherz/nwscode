#!/usr/bin/env python
# encoding: utf-8
"""
A parser for the *Universal Geographic Code*.

Created by Alexander Ross on 2006-07-20.
Copyright (c) 2006 NOAA's National Weather Service. All rights reserved.
"""

__all__ = ["UgcError", "Ugc"]

import re
from nwscode import NwsCode, NwsCodeError
from misc import Bunch, RelativeTime

IDENT = r"[A-Z]{3}"
NUMBER = r"[0-9]{3}"
DELIM = r">|\-\n?"
AREA = r"%s(?:%s(?:%s))+" % (IDENT, NUMBER, DELIM)
TIME = r"[0-9]{6}"
UGC = r"^((?:%s)+)(%s)[\-]$" % (AREA, TIME)

class UgcError(NwsCodeError):
    pass

class Ugc(NwsCode):
    """
    A *Universal Geographic Code* parser, inherits from `NwsCode`.
    
    For a full description of the UGC format see the National Weather
    Service's UGC Directive:
    
        http://www.nws.noaa.gov/directives/sym/pd01017002curr.pdf
    
    Attributes:
        
        ``raw``
            The raw UGC string, undecoded.
        
        ``code``
            Provides access to the individual code groups.  In this case,
            ``area`` and ``expiration``.
        
        ``areas``
            A list of affected areas.
        
        ``expiration``
            The product expiration time.
    """
    
    pattern = re.compile(UGC, re.M)
    error = UgcError
    
    def _process_matches(self, matches):
        self.areas = self._expand_area(matches[0])
        time_string = matches[1]
        day, hour, minute = time_string[:2], time_string[2:4], time_string[4:]
        self.expiration = RelativeTime(day, hour, minute)
    
    def _expand_area(area_string):
        areas = []
        for m in re.compile(r"(%s)" % AREA, re.M).finditer(area_string):
            area = m.group(0).replace('\n', '')
            ident, numbers = area[:3], area[3:]
            numbers = numbers.strip('-').split('-')
            buf = []
            for num in numbers:
                if ">" in num:
                    first, last = num.split(">")
                    first, last = int(first), int(last)
                    buf.extend(["%03i" % n for n in range(first, last + 1)])
                else:
                    buf.append(num)
            areas.extend([ident + num for num in buf])
        return areas
    _expand_area = staticmethod(_expand_area)
