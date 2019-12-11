#!/usr/bin/env python
# encoding: utf-8
"""
Tests for the ``AwipsId`` in ``nwscode.awipsid``.

Created by Alexander Ross on 2006-08-01.
Copyright (c) 2006 NOAA's National Weather Service. All rights reserved.
"""

from py.test import raises
from nwscode.awipsid import AwipsId, AwipsIdError

def test_awipsid():
    aw = AwipsId("ZFPAFG")
    assert aw.raw == "ZFPAFG"
    assert aw.category == "ZONE FORECAST PRODUCT"
    assert aw.designator == "AFG"
    assert aw.code.category == "ZFP"
    assert aw.code.designator == "AFG"

def test_good():
    a = AwipsId("ZFPAFG")
    assert a.raw == "ZFPAFG"
    a = AwipsId("FFAREV")
    assert a.raw == "FFAREV"
    a = AwipsId("NPWPSR")
    assert a.raw == "NPWPSR"
    a = AwipsId("NPWPS ")
    assert a.raw == "NPWPS "

def test_bad():
    raises(AwipsIdError, AwipsId, "ZFPAF")
    raises(AwipsIdError, AwipsId, "FFRES2")
    raises(AwipsIdError, AwipsId, "NPWPSR4")