# -*- coding: utf-8 -*-
#
# Copyright (c) 2014-2016 Scaleway and Contributors. All Rights Reserved.
#                         Kevin Deldycke <kdeldycke@scaleway.com>
#                         Gilles Dartiguelongue <gdartiguelongue@scaleway.com>
#
# Licensed under the BSD 2-Clause License (the "License"); you may not use this
# file except in compliance with the License. You may obtain a copy of the
# License at https://opensource.org/licenses/BSD-2-Clause

""" Port range utilities and helpers.
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import math
from collections import Iterable

try:
    from itertools import imap as iter_map
except ImportError:  # pragma: no cover
    iter_map = map

try:
    basestring
except NameError:  # pragma: no cover
    basestring = (str, bytes)  # pylint: disable=C0103

__version__ = '2.1.1'


class PortRange(object):

    """ Port range with support of a CIDR-like (binary) notation.

    In strict mode (disabled by default) we'll enforce the following rules:
        * port base must be a power of two (offsets not allowed);
        * port range must be within the 1-65535 inclusive range.

    This mode can be disabled on object creation.
    """

    # Separators constants for CIDR and range notation.
    CIDR_SEP = '/'
    RANGE_SEP = '-'

    # Max port length, in bits.
    port_length = 16
    # Max port range integer values
    port_min = 1
    port_max = (2 ** port_length) - 1

    # Base values on which all other properties are computed.
    port_from = None
    port_to = None

    def __init__(self, port_range, strict=False):
        """ Set up class with a port_from and port_to integer. """
        self.strict = strict
        self.port_from, self.port_to = self.parse(port_range)

    def parse(self, port_range):
        """ Parse and normalize a string or iterable into a port range. """
        # Any string containing a CIDR separator is parsed as a CIDR-like
        # notation, others as a range or single port.
        cidr_notation = False
        if isinstance(port_range, basestring):
            cidr_notation = self.CIDR_SEP in port_range
            separator = self.CIDR_SEP if cidr_notation else self.RANGE_SEP
            port_range = port_range.split(separator, 1)

        # We expect here a list of elements castable to integers.
        if not isinstance(port_range, Iterable):
            port_range = [port_range]
        try:
            port_range = list(iter_map(int, port_range))
        except TypeError:
            raise ValueError("Can't parse range as a list of integers.")

        # At this point we should have a list of one or two integers.
        if not 0 < len(port_range) < 3:
            raise ValueError("Expecting a list of one or two elements.")

        # Transform CIDR notation into a port range and validates it.
        if cidr_notation:
            base, prefix = port_range
            port_range = self._cidr_to_range(base, prefix)

        # Let the parser fix a reverse-ordered range in non-strict mode.
        if not self.strict:
            port_range.sort()

        # Get port range bounds.
        port_from = port_range[0]
        # Single port gets their upper bound set to None.
        port_to = port_range[1] if len(port_range) == 2 else None

        # Validate constraints in strict mode.
        if self.strict:
            # Disallow out-of-bounds values.
            if not (self.port_min <= port_from <= self.port_max) or (
                    port_to is not None and not (
                        self.port_min <= port_to <= self.port_max)):
                raise ValueError("Out of bounds.")
            # Disallow reversed range.
            if port_to is not None and port_from > port_to:
                raise ValueError("Invalid reversed port range.")

        # Clamp down lower bound, then cap it.
        port_from = min([max([port_from, self.port_min]), self.port_max])

        # Single port gets its upper bound aligned to its lower one.
        if port_to is None:
            port_to = port_from

        # Cap upper bound.
        port_to = min([port_to, self.port_max])

        return port_from, port_to

    def __repr__(self):
        """ Print all components of the range. """
        return (
            '{}(port_from={}, port_to={}, base={}, offset={}, prefix={}, '
            'mask={}, is_single_port={}, is_cidr={})').format(
                self.__class__.__name__, self.port_from, self.port_to,
                self.base, self.offset, self.prefix, self.mask,
                self.is_single_port, self.is_cidr)

    def __str__(self):
        """ Return the most appropriate string representation. """
        if self.is_single_port:
            return str(self.port_from)
        try:
            return self.cidr_string
        except ValueError:
            return self.range_string

    @property
    def cidr_string(self):
        """ Return a clean CIDR-like notation if possible. """
        if not self.is_cidr:
            raise ValueError(
                "Range can't be rendered using a CIDR-like notation.")
        return '{}{}{}'.format(self.base, self.CIDR_SEP, self.prefix)

    @property
    def range_string(self):
        """ Return a clean range notation. """
        return '{}{}{}'.format(self.port_from, self.RANGE_SEP, self.port_to)

    @classmethod
    def _is_power_of_two(cls, value):
        """ Helper to check if a value is a power of 2. """
        return math.log(value, 2) % 1 == 0

    @classmethod
    def _nearest_power_of_two(cls, value):
        """ Return nearest power of 2. """
        return int(2 ** math.floor(math.log(value, 2)))

    @classmethod
    def _mask(cls, prefix):
        """ Compute the mask. """
        return cls.port_length - prefix

    @classmethod
    def _raw_upper_bound(cls, base, prefix):
        """ Compute a raw upper bound. """
        return base + (2 ** cls._mask(prefix)) - 1

    def _cidr_to_range(self, base, prefix):
        """ Transform a CIDR-like notation into a port range. """
        # Validates base and prefix values.
        if not self.port_min <= base <= self.port_max:
            raise ValueError("Port base out of bounds.")
        if not 1 <= prefix <= self.port_length:
            raise ValueError("CIDR-like prefix out of bounds.")

        # Disallow offsets in strict mode.
        if (self.strict and prefix != self.port_length
                and not self._is_power_of_two(base)):
            raise ValueError("Port base is not a power of two.")

        port_from = base
        port_to = self._raw_upper_bound(base, prefix)
        return [port_from, port_to]

    @property
    def bounds(self):
        """ Return lower and upper bounds of the port range. """
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
        return self.port_length - int(math.log(port_delta, 2))

    @property
    def mask(self):
        """ Port range binary mask, based on CIDR-like prefix. """
        return self._mask(self.prefix) if self.prefix else None

    @property
    def cidr(self):
        """ Return components of the CIDR-like notation. """
        return self.base, self.prefix

    @property
    def is_single_port(self):
        """ Is the range a single port? """
        return True if self.port_from == self.port_to else False

    @property
    def is_cidr(self):
        """ Is the range can be expressed using a CIDR-like notation? """
        return True if self.prefix is not None else False
