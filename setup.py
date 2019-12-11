#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='nwscode',
      description='Decoders for various codes used in NWS products.',
      author='Alex Ross',
      author_email='alex.j.ross@gmail.com',
      packages=['nwscode'])