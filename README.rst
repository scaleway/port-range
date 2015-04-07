port-range
==========

Port range with support of CIDR-like notation.

.. image:: https://img.shields.io/pypi/v/port-range.svg?style=flat
    :target: https://pypi.python.org/pypi/port-range
    :alt: Last release
.. image:: https://img.shields.io/travis/scaleway/port-range/develop.svg?style=flat
    :target: https://travis-ci.org/scaleway/port-range
    :alt: Unit-tests status
.. image:: https://img.shields.io/coveralls/scaleway/port-range/develop.svg?style=flat
    :target: https://coveralls.io/r/scaleway/port-range?branch=develop
    :alt: Coverage Status
.. image:: https://img.shields.io/requires/github/scaleway/port-range/master.svg?style=flat
    :target: https://requires.io/github/scaleway/port-range/requirements/?branch=master
    :alt: Requirements freshness
.. image:: https://img.shields.io/pypi/l/port-range.svg?style=flat
    :target: http://opensource.org/licenses/BSD-2-Clause
    :alt: Software license
.. image:: https://img.shields.io/pypi/dm/port-range.svg?style=flat
    :target: https://pypi.python.org/pypi/port-range#downloads
    :alt: Popularity


Features
--------

Support CIDR-like notation:

.. code-block:: python

    >>> from port_range import PortRange
    >>> pr = PortRange('1027/15')
    >>> pr.port_from
    1027
    >>> pr.port_to
    1028
    >>> pr.bounds
    (1027, 1028)

Parse and normalize port ranges:

.. code-block:: python

    >>> pr = PortRange(' 4242-42 ')
    >>> pr.bounds
    (42, 4242)
    >>> str(pr)
    '42-4242'

Access to decimal-representation properties:

.. code-block:: python

    >>> pr = PortRange('1027/15')
    >>> pr.base
    1027
    >>> pr.prefix
    15
    >>> pr.mask
    1
    >>> pr.offset
    3


License
-------

This software is licensed under the `BSD 2-Clause License`_.

.. _BSD 2-Clause License: https://github.com/scaleway/port-range/blob/develop/LICENSE.rst
