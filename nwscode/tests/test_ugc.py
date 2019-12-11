#!/usr/bin/env python
# encoding: utf-8
"""
Tests for ``Ugc`` in ``nwscode.ugc``.

Created by Alexander Ross on 2006-07-26.
Copyright (c) 2006 NOAA's National Weather Service. All rights reserved.
"""

from py.test import raises
from nwscode.ugc import Ugc, UgcError
from nwscode.misc import RelativeTime

def test_ugc():
    u = Ugc('NCZ001>006-018>020-VAZ007-009>020-022>024-032>035-043>047-\n'\
            '058-059-WVZ042>045-142030-')
    assert u.area == ['NCZ001', 'NCZ002', 'NCZ003', 'NCZ004', 'NCZ005',
                      'NCZ006', 'NCZ018', 'NCZ019', 'NCZ020', 'VAZ007',
                      'VAZ009', 'VAZ010', 'VAZ011', 'VAZ012', 'VAZ013',
                      'VAZ014', 'VAZ015', 'VAZ016', 'VAZ017', 'VAZ018',
                      'VAZ019', 'VAZ020', 'VAZ022', 'VAZ023', 'VAZ024',
                      'VAZ032', 'VAZ033', 'VAZ034', 'VAZ035', 'VAZ043',
                      'VAZ044', 'VAZ045', 'VAZ046', 'VAZ047', 'VAZ058',
                      'VAZ059', 'WVZ042', 'WVZ043', 'WVZ044', 'WVZ045']
    assert u.expiration.day == 14
    assert u.expiration.hour == 20
    assert u.expiration.minute == 30
    raises(ValueError, lambda: u.expiration < RelativeTime(15, 20, 30))

def test_good():
    Ugc('WAZ001>023-039-040-292300-')
    Ugc('WAZ024>038-041>044-292230-')
    Ugc('MEZ001-003-004-291600-')
    Ugc('MEZ002-005-006-010-291600-')
    Ugc('NCZ001>006-018>020-VAZ007-009>020-022>024-032>035-043>047-\n'\
        '058-059-WVZ042>045-142030-')

def test_bad():
    raises(UgcError, Ugc, 'WAZ001>02-039-040-292300-')
    raises(UgcError, Ugc, 'WAZ024>038041>044-292230-')
    raises(UgcError, Ugc, 'MEZ001-003-004-91600-')
    raises(UgcError, Ugc, 'MZ002-005-006-010-291600-')
    raises(UgcError, Ugc, 'NCZ001>006-018>020-VAZ007-009\n'\
                          '020-022>024-032>035-043>047-\n'\
                          '058-059-WVZ042>045-142030-')
