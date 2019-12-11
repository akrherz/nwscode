#!/usr/bin/env python
# encoding: utf-8
"""
Tests for ``Hvtec`` in ``nwscode.hvtec``.

Created by Alexander Ross on 2006-07-26.
Copyright (c) 2006 NOAA's National Weather Service. All rights reserved.
"""

try:
    from datetime import datetime
except ImportError:
    from nwscode.pydatetime import datetime

from py.test import raises
from nwscode.hvtec import Hvtec, HvtecError

def test_code():
    hv = Hvtec('/DEMI4.1.ER.030509T2100Z.030510T0300Z.030510T0900Z.NO/')
    # parsed codes
    assert hv.siteid == 'DEMI4'
    assert hv.floodseverity == 'Minor'
    assert hv.immediatecause == 'Excessive Rainfall'
    assert hv.floodbegin == datetime(2003, 5, 9, 21, 00)
    assert hv.floodcrest == datetime(2003, 5, 10, 3, 00)
    assert hv.floodend == datetime(2003, 5, 10, 9, 00)
    assert hv.recordstatus == 'A record flood is not expected.'
    # raw code access
    assert hv.code.siteid == 'DEMI4'
    assert hv.code.floodseverity == '1'
    assert hv.code.immediatecause == 'ER'
    assert hv.code.floodbegin == '030509T2100Z'
    assert hv.code.floodcrest == '030510T0300Z'
    assert hv.code.floodend == '030510T0900Z'
    assert hv.code.recordstatus == 'NO'

def test_good():
    h = Hvtec("/BRKS2.2.ER.041216T1600Z.041218T1600Z.041219T1200Z.NO/")
    assert h.raw == "/BRKS2.2.ER.041216T1600Z.041218T1600Z.041219T1200Z.NO/"
    h = Hvtec("/00000.0.ER.000000T0000Z.000000T0000Z.000000T0000Z.OO/")
    assert h.raw == "/00000.0.ER.000000T0000Z.000000T0000Z.000000T0000Z.OO/"
    h = Hvtec("/DERS2.3.ER.041217T0400Z.041218T1700Z.041220T0200Z.NO/")
    assert h.raw == "/DERS2.3.ER.041217T0400Z.041218T1700Z.041220T0200Z.NO/"
    h = Hvtec("/AKRI4.2.ER.041217T0400Z.041218T1900Z.041220T1200Z.NO/")
    assert h.raw == "/AKRI4.2.ER.041217T0400Z.041218T1900Z.041220T1200Z.NO/"
    h = Hvtec("/GLDI2.1.ER.040426T2000Z.040430T1100Z.040503T1500Z.NO/")
    assert h.raw == "/GLDI2.1.ER.040426T2000Z.040430T1100Z.040503T1500Z.NO/"

def test_bad():
    raises(HvtecError, Hvtec, 
                     "/BRKS.2.ER.041216T1600Z.041218T1600Z.041219T1200Z.NO/")
    raises(HvtecError, Hvtec, 
                     "/00000.0.ER.0000000000Z.000000T0000Z.000000T0000Z.OO/")
    raises(HvtecError, Hvtec, 
                     "/DERS2.3.ER.04121T0400Z.041218T1700Z.041220T0200Z.NO/")
    raises(HvtecError, Hvtec, 
                     "/AKRI4.2.ER041217T0400Z.041218T1900Z.041220T1200Z.NO/")
    raises(HvtecError, Hvtec, 
                     "/GLDI2.1.ER.040426T2000Z.040430T1100Z.040503T1500Z.NO")
