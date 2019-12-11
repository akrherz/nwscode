#!/usr/bin/env python
# encoding: utf-8
"""
Tests for ``Wmo`` in ``nwscode.wmo``.

Created by Alexander Ross on 2006-07-27.
Copyright (c) 2006 NOAA's National Weather Service. All rights reserved.
"""

from py.test import raises
from nwscode.wmo import WmoHeader, WmoError

def test_wmoheader():
    w = WmoHeader('FZAK52 PAFG 271242 AAA')
    assert w.designator == 'FZAK52'
    assert w.station == 'PAFG'
    assert w.issuance.day == 27
    assert w.issuance.hour == 12
    assert w.issuance.minute == 42
    print w.addendum
    assert w.addendum == 'AAA'

def test_good():
    assert WmoHeader('SMIN04 DEMS 171200 RRA').raw == 'SMIN04 DEMS 171200 RRA'
    assert WmoHeader('SMIN04 DEMS 171200').raw == 'SMIN04 DEMS 171200'
    assert WmoHeader('SMIN04 DEMS 171200 CCA').raw == 'SMIN04 DEMS 171200 CCA'
    assert WmoHeader('FPJM20 MKJP 171200').raw == 'FPJM20 MKJP 171200'
    assert WmoHeader('FPJM20 MKJP 171200 AAA').raw == 'FPJM20 MKJP 171200 AAA'

def test_bad():
    raises(WmoError, WmoHeader, 'SMIN0 DEMS 171200 RRA')
    raises(WmoError, WmoHeader, 'SMIN04 DDEMS 171200')
    raises(WmoError, WmoHeader, 'SMIE01 EDB 1711200')
    raises(WmoError, WmoHeader, 'SMIN04 DEMS 171200 CCA0')
    raises(WmoError, WmoHeader, 'FPJM20 MKJP 17200')
    raises(WmoError, WmoHeader, 'PJM20 MKJP 171200 AAA')