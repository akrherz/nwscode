#!/usr/bin/env python
# encoding: utf-8
"""
A basic code class.  Don't use it, extend it.

Created by Alexander Ross on 2006-07-20.
Copyright (c) 2006 NOAA's National Weather Service. All rights reserved.
"""

__all__ = ["NwsCodeError", "NwsCode"]

import re

class NwsCodeError(Exception):
    pass

class NwsCode(object):
    """
    Base `NwsCode` class, represents a generic code string.
    """
    # regular expression matching a code.
    pattern = re.compile(r"^.*$")
    error = NwsCodeError
    interpreted = {}
    def __init__(self, code_string=''):
        """
        Create an instance of the NwsCode class.

        The parameter `code_string` should be a coded string.
        """
        self.raw = code_string
        match = self.pattern.match(code_string)
        if match:
            self._process_matches(match.groups())
        else:
            raise self.error("Invalid code: %s" % self.raw)

    def _interpret(self, element, code):
        # make sure to define self.intepreted before calling this method.
        assert element in self.interpreted
        if code in self.interpreted[element]:
            return self.interpreted[element][code]
        else:
            raise self.error("Invalid code '%s' for `%s`." % (code, element))

    def _process_matches(self, matches):
        # subclasses need to override this method.
        pass

    def valid(cls, code_string):
        """True if `code_string` is matched by `self.pattern`."""
        return bool(self.pattern.match(code_string))
    valid = classmethod(valid)

    def __str__(self):
        return self.raw

    def __repr__(self):
        return str(self.__class__.__name__) + '(' + `self.raw` + ')'
