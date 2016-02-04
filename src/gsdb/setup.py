#!/usr/bin/env python

sdict = {
    'name': 'gsdb',
    'version': "0.1.2",
    'packages': ['gsdb'],
    'zip_safe': False,
    'install_requires': ['mongoengine'],
    'author': 'Lichun',
    'classifiers': [
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python']
}

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(**sdict)
