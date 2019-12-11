#!/usr/bin/env python
# encoding: utf-8
"""
Tests for ``Pvtec`` in ``nwscode.pvtec``.

Created by Alexander Ross on 2006-07-26.
Copyright (c) 2006 NOAA's National Weather Service. All rights reserved.
"""

try:
    from datetime import datetime
except ImportError:
    from nwscode.pydatetime import datetime

from py.test import raises
from nwscode.nwscode import NwsCodeError
from nwscode.pvtec import Pvtec

def test_code():
    pv = Pvtec('/O.NEW.KBMX.FL.W.0098.041226T1800Z-041227T0000Z/')
    assert pv.fixedid == 'Operational Product'
    assert pv.action == 'New'
    assert pv.officeid == 'KBMX'
    assert pv.phenomena == 'Flood'
    assert pv.significance == 'Warning'
    assert pv.etn == 98
    print pv.eventbegin
    assert pv.eventbegin == datetime(2004, 12, 26, 18, 00)
    assert pv.eventend == datetime(2004, 12, 27, 00, 00)
    assert pv.code.fixedid == 'O'
    assert pv.code.action == 'NEW'
    assert pv.code.officeid == 'KBMX'
    assert pv.code.phenomena == 'FL'
    assert pv.code.significance == 'W'
    assert pv.code.etn == '0098'
    assert pv.code.eventbegin == '041226T1800Z'
    assert pv.code.eventend == '041227T0000Z'

def test_good():
    # strings that should parse
    Pvtec('/O.NEW.KBMX.FL.W.0097.041224T0300Z-041227T0300Z/')
    Pvtec('/O.ROU.KBMX.HY.S.0000.000000T0000Z-000000T0000Z/')
    Pvtec('/O.NEW.KBMX.FL.W.0098.041226T1800Z-041227T0000Z/')
    Pvtec('/O.CAN.KOUN.IS.W.0003.000000T0000Z-040129T0000Z/')
    Pvtec('/O.NEW.KOUN.WS.W.0006.040128T0530Z-040129T0000Z/')

def test_bad():
    # strings that should not parse
    raises(NwsCodeError, Pvtec, '/O.NEW.KBMX.FL.W.0097.041224T0300-041227T0300Z/')
    raises(NwsCodeError, Pvtec, '/O.ROT.KBMX.HY.S.000.000000T0000Z-000000T0000Z/')
    raises(NwsCodeError, Pvtec, '/O.NEW.KBMX.FL.W.0098.041226I1800Z-041227T0000Z/')
    raises(NwsCodeError, Pvtec, '/K.CAN.KOUN.IS.W.0003.000000T0000Z-040129T0000Z/')
    raises(NwsCodeError, Pvtec, '/O.NEW.KOUN.WS.C.0006.040128T0530Z-040129T0000Z/')
    raises(NwsCodeError, Pvtec, '/ONEW.KOUN.WS.C.0006.040128T0530Z-040129T0000Z/')
    raises(NwsCodeError, Pvtec, '/O.NEW.KOUN.WP.C.0006.040128T0530Z-040129T0000Z/')
