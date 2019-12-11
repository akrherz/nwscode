#!/usr/bin/env python
# encoding: utf-8
"""
Tools for working with NWS product texts.

Created by Alexander Ross on 2006-07-17.
Copyright (c) 2006 NOAA's National Weather Service. All rights reserved.
"""

import re

from nwscode import NwsCode
from wmo import WmoHeader
from awipsid import AwipsId
from ugc import Ugc
from pvtec import Pvtec
from hvtec import Hvtec

class ProductError(Exception):
    pass

class Product (object):
    def __init__(self, text):
        self.text = text.strip().replace("\r\n", "\n")
        m = Ugc.pattern.search(text)
        if not m:
            raise ProductError("Product does not contain a UGC code.")
        self.header = Header(self.text[:m.start()].strip())
        body = self.text[m.start():].strip()
        self.segments = []
        segment_texts = Segment.pattern.split(body)
        self.footer = Footer(segment_texts.pop())
        for seg_text in segment_texts:
            events = []
            seg_text = seg_text.strip()
            if not seg_text:
                continue
            try:
                seg = Segment(seg_text)
            except SegmentError:
                pass
            else:
                self.segments.append(seg)
    
    def __str__(self):
        lines = [str(self.header)]
        if self.segments:
            lines.extend([str(ev) for ev in self.segments])
        lines.append(str(self.footer))
        return '\n'.join(lines)
    

class Header(object):
    """
    ``Product Header``
    """
    def __init__(self, text):
        self.text = text.strip()
        text = text.split("\n")
        try:
            self.wmo = WmoHeader(text[0])
            self.awipsid = AwipsId(text[1])
        except:
            raise ProductError()
    
    def __str__(self):
        return self.text
    

class Footer(object):
    def __init__(self, text):
        self.text = text.strip()
    def __str__(self):
        return self.text
    

class SegmentError(ProductError):
    pass

SEGMENT = r"^\$\$$"
class Segment(object):
    """ Segment wraps a text segment.
        
        Attribute:
        
            ``ugc``
                ugc code for this segment.
        
            ``text``
                the actual segment text.
        
            ``events``
                a list of any events in the segment.
        
            ``forecasts``
                list of forecasts in the segment.  Ordered nearest to farthest
                from now.
            
            ``headlines``
                list of headlines in the segment.
        
    """
    pattern = re.compile(SEGMENT, re.MULTILINE|re.DOTALL)
    def __init__(self, text):
        self.text = text
        # parse events.
        self.events = []
        m = Ugc.pattern.search(self.text)
        if not m:
            raise SegmentError("Segment does not have a UGC code.")
        self.ugc = Ugc(self.text[m.start():m.end()])
        for line in self.text.split('\n'):
            if Pvtec.pattern.match(line):
                self.events.append(Event(self.ugc, Pvtec(line)))
            elif Hvtec.pattern.match(line):
                self.events[-1].hvtec = Hvtec(line)
        # parse forecasts.
        self.forecasts = []
        fcst_pat = re.compile(r"(?m)^\.[A-Z ]+?[\.]{3}.*(?:\n(?:[A-Z0-9].*)*)*")
        for m in fcst_pat.finditer(self.text):
            fcst = m.group(0).replace("\n", " ").strip()
            self.forecasts.append(fcst)
        # parse headlines.
        self.headlines = []
        headline_pat = re.compile(r"(?ms)^[\.]{3}[A-Z0-9 \n]*[\.]{3}$")
        for m in headline_pat.finditer(self.text):
            headline = m.group(0).replace("\n", " ").strip()
            self.headlines.append(headline)
        # we've got to handle short-fuse products seperately.  These don't
        # even have a headline in them so we have to generate them.
        short_fuse = re.compile(r"(?m)^\* (?:SEVERE THUNDERSTORM|TORNADO|(?:FLASH )?FLOOD) (?:WARNING|WATCH|ADVISORY) FOR[\.]*(?:\n[A-Z0-9 .]+)$")
        for m in short_fuse.finditer(self.text):
            headline = m.group(0)
            headline = headline.replace('\n', ' ')
            headline = headline.lstrip("* ")
            headline = headline.replace("...", "")
            headline = re.compile("  +").sub(' ', headline)
            headline = "..." + headline + "..."
            self.headlines.append(headline)
    
    def __str__(self):
        return self.text
    

class Event(object):
    """
    ``Event`` wraps instances of a UGC, a PVTEC, and (optionally) an HVTEC
    object.  The attributes of each of those objects are accessible through
    the Event object.  The event object is intended as a minimal container
    for these three objects.
    """
     
    def __init__(self, ugc, pvtec, hvtec=None):
        self.ugc = ugc
        self.pvtec = pvtec
        self.hvtec = hvtec
    
    def __getattr__(self, name):
        if hasattr(self.ugc, name):
            return getattr(self.ugc, name)
        elif hasattr(self.pvtec, name):
            return getattr(self.pvtec, name)
        if self.hvtec and hasattr(self.hvtec, name):
            return getattr(self.hvtec, name)
        raise AttributeError
    
    def __str__(self):
        s = [str(self.ugc), str(self.pvtec)]
        if self.hvtec:
            s.append(str(self.hvtec))
        return '\n'.join(s)
    
    def __repr__(self):
        return repr(str(self))
    

if __name__ == "__main__":
    import sys
    prod = Product(file(sys.argv[1], 'r').read())
    print prod.segments[-1].forecasts
    print prod.segments[-1].events
    print prod.segments[-1].headlines
    print prod.segments[-1].hazard_keywords