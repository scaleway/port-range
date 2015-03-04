# -*- coding: utf-8 -*-
#
# Copyright (c) 2014-2015 Online SAS and Contributors. All Rights Reserved.
#                         Kevin Deldycke <kdeldycke@ocs.online.net>
#                         Gilles Dartiguelongue <gdartiguelongue@ocs.online.net>
#
# Licensed under the BSD 2-Clause License (the "License"); you may not use this
# file except in compliance with the License. You may obtain a copy of the
# License at http://opensource.org/licenses/BSD-2-Clause

""" Port range utilities and helpers.
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import math

try:
    basestring
except NameError:  # pragma: no cover
    basestring = (str, bytes)  # pylint: disable=C0103

try:
    from itertools import imap as iter_map
except ImportError:  # pragma: no cover
    iter_map = map


__version__ = '1.0.1'


class PortRange(object):
    """ Port range with support of a CIDR-like (binary) notation.

    In strict mode (disabled by default) we'll enforce the following rules:
        * port base must be a power of two (offsets not allowed);
        * port CIDR should not produce overflowing upper bound.

    This mode can be disabled on object creation.
    """
    # Separators constants
    CIDR_SEP = '/'
    RANGE_SEP = '-'

    # Max port lenght, in bits
    port_lenght = 16
    # Max port range integer values
    port_min = 1
    port_max = (2 ** port_lenght) - 1

    # Base values on which all other properties are computed.
    port_from = None
    port_to = None

    def __init__(self, port_range, strict=False):
        """ Set up class with a port_from and port_to integer. """
        self.port_from, self.port_to = self.parse(port_range, strict=strict)

    def parse(self, port_range, strict=False):
        """ Parse and normalize port range string into a port range. """
        if isinstance(port_range, basestring) and self.CIDR_SEP in port_range:
            base, prefix = self.parse_cidr(port_range, strict)
            port_from, port_to = self._cidr_to_range(base, prefix)
        else:
            port_from, port_to = self.parse_range(port_range)
        if not port_from or not port_to:
            raise ValueError("Invalid ports.")
        # Check upper bound
        if strict:
            # Disallow overflowing upper bound
            if port_to > self.port_max:
                raise ValueError("Overflowing upper bound.")
        else:
            # Cap upper bound
            port_to = port_to if port_to < self.port_max else self.port_max
        return port_from, port_to

    def parse_cidr(self, port_range, strict=False):
        """ Split a string and extract port base and CIDR prefix.

        Always returns a list of 2 integers. Defaults to None.
        """
        # Separate base and prefix
        elements = list(iter_map(int, port_range.split(self.CIDR_SEP, 2)))
        elements += [None, None]
        base, prefix = elements[:2]
        # Normalize prefix value
        if prefix is None:
            prefix = self.port_lenght
        # Validates base and prefix values
        if not base or base < self.port_min or base > self.port_max:
            raise ValueError("Invalid port base.")
        if not prefix or prefix < 1 or prefix > self.port_lenght:
            raise ValueError("Invalid CIDR-like prefix.")
        # Enable rigorous rules
        if strict:
            # Disallow offsets
            if prefix != self.port_lenght and not self._is_power_of_two(base):
                raise ValueError("Port base is not a power of Two.")
        return base, prefix

    def parse_range(self, port_range):
        """ Normalize port range to a sorted list of no more than 2 integers.

        Excludes None values while parsing.
        """
        if isinstance(port_range, basestring):
            port_range = port_range.split(self.RANGE_SEP, 2)
        if not isinstance(port_range, (set, list, tuple)):
            port_range = [port_range]
        port_range = [int(port)
                      for port in port_range
                      if port and int(port)][:2]
        port_range.sort()
        # Fill out missing slots by None values
        port_range += [None] * (2 - len(port_range))
        port_from, port_to = port_range
        if not port_from or port_from < self.port_min or \
                port_from > self.port_max:
            raise ValueError("Invalid port range lower bound.")
        if not port_to:
            port_to = port_from
        return port_from, port_to

    def __repr__(self):
        """ Print all components of the range. """
        return '{}(port_from={}, port_to={}, base={}, offset={}, prefix={}, ' \
            'mask={})'.format(self.__class__.__name__, self.port_from,
                              self.port_to, self.base, self.offset,
                              self.prefix, self.mask)

    def __str__(self):
        """ Returns the most appropriate string representation. """
        if self.is_single_port:
            return str(self.port_from)
        return self.cidr_string if self.is_cidr else self.range_string

    @property
    def cidr_string(self):
        """ Returns a clean CIDR-like notation. """
        return '{}{}{}'.format(self.base, self.CIDR_SEP, self.prefix)

    @property
    def range_string(self):
        """ Returns a clean range notation. """
        return '{}{}{}'.format(self.port_from, self.RANGE_SEP, self.port_to)

    @classmethod
    def _is_power_of_two(cls, value):
        """ Helper to check if a value is a power of 2. """
        return math.log(value, 2) % 1 == 0

    @classmethod
    def _nearest_power_of_two(cls, value):
        """ Returns nearsest power of 2. """
        return int(2 ** math.floor(math.log(value, 2)))

    @classmethod
    def _mask(cls, prefix):
        """ Compute the mask. """
        return cls.port_lenght - prefix

    @classmethod
    def _raw_upper_bound(cls, base, prefix):
        """ Compute a raw upper bound. """
        return base + (2 ** cls._mask(prefix)) - 1

    @classmethod
    def _cidr_to_range(cls, base, prefix):
        """ Transform a CIDR-like notation into a port range. """
        port_from = base
        port_to = cls._raw_upper_bound(base, prefix)
        return port_from, port_to

    @property
    def bounds(self):
        """ Returns lower and upper bounds of the port range. """
        return self.port_from, self.port_to

    @property
    def base(self):
        """ Alias to port_from, used as a starting point for CIDR notation. """
        return self.port_from

    @property
    def offset(self):
        """ Port base offset from its nearest power of two. """
        return self.base - self._nearest_power_of_two(self.base)

    @property
    def prefix(self):
        """ A power-of-two delta means a valid CIDR-like prefix. """
        # Check that range delta is a power of 2
        port_delta = self.port_to - self.port_from + 1
        if not self._is_power_of_two(port_delta):
            return None
        return self.port_lenght - int(math.log(port_delta, 2))

    @property
    def mask(self):
        """ Port range binary mask, based on CIDR-like prefix. """
        return self._mask(self.prefix) if self.prefix else None

    @property
    def cidr(self):
        """ Returns components of the CIDR-like notation. """
        return self.base, self.prefix

    @property
    def is_single_port(self):
        """ Is the range a single port ? """
        return True if self.port_from == self.port_to else False

    @property
    def is_cidr(self):
        """ Is the range can be expressed using a CIDR-like notation. """
        return True if self.prefix is not None else False
