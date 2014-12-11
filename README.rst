port-range
==========

Port range with support of CIDR-like notation.

.. image:: https://badge.fury.io/py/port-range.svg
    :target: http://badge.fury.io/py/port-range
    :alt: Last release
.. image:: https://travis-ci.org/online-labs/port-range.svg?branch=develop
    :target: https://travis-ci.org/online-labs/port-range
    :alt: Unit-tests status
.. image:: https://requires.io/github/online-labs/port-range/requirements.svg?branch=master
    :target: https://requires.io/github/online-labs/port-range/requirements/?branch=master
    :alt: Requirements freshness
.. image:: http://img.shields.io/pypi/l/port-range.svg
    :target: http://opensource.org/licenses/BSD-2-Clause
    :alt: Software license
.. image:: http://img.shields.io/pypi/dm/port-range.svg
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

.. _BSD 2-Clause License: https://github.com/online-labs/ocs-sdk/blob/develop/LICENSE.rst