#!/usr/bin/env python
# encoding: utf-8
"""
A collection of parsers for various NWS coded strings.

Created by Alexander Ross on 2006-07-15.
Copyright (c) 2006 NOAA's National Weather Service. All rights reserved.
"""

# Weather Service codes depend on time in UTC.
import os; os.environ["TZ"] = "UTC"
