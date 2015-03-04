#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2014-2015 Online SAS and Contributors. All Rights Reserved.
#                         Kevin Deldycke <kdeldycke@ocs.online.net>
#
# Licensed under the BSD 2-Clause License (the "License"); you may not use this
# file except in compliance with the License. You may obtain a copy of the
# License at http://opensource.org/licenses/BSD-2-Clause

import os
import re

from setuptools import setup, find_packages


MODULE_NAME = 'port_range'


def get_version():

    with open(os.path.join(
        os.path.dirname(__file__), MODULE_NAME, '__init__.py')
    ) as init:

        for line in init.readlines():
            res = re.match(r'__version__ *= *[\'"]([0-9\.]*)[\'"]$', line)
            if res:
                return res.group(1)


def get_long_description():
    readme = os.path.join(os.path.dirname(__file__), 'README.rst')
    changes = os.path.join(os.path.dirname(__file__), 'CHANGES.rst')
    return open(readme).read() + '\n' + open(changes).read()


setup(
    name='port-range',
    version=get_version(),
    description="Port range with support of CIDR-like notation",
    long_description=get_long_description(),

    author='Online Labs',
    author_email='opensource@labs.online.net',
    url='http://github.com/online-labs/port-range',
    license='BSD',

    install_requires=[],

    packages=find_packages(),

    tests_require=[],
    test_suite=MODULE_NAME + '.tests',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Networking',
    ],

    entry_points={
        'console_scripts': [],
    }
)
