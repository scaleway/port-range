# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import math
import itertools


class PortRange(object):
    """ Port range with support of a CIDR-like (binary) notation.

    In strict mode (disabled by default) we'll enforce the following rules:
        * port base must be a power of two (unless its CIDR is 32).
        * port CIDR should not produce overflowing upper bound.

    This mode can be disabled on object creation.
    """

    # Max port lenght, in bytes
    port_lenght = 16
    # Max port range, in integers
    port_min = 1
    port_max = (2 ** port_lenght) - 1

    def __init__(self, port_range, strict=False):
        """ Parse and normalize port range string into a base and a prefix.
        """
        # Separate base and prefix
        if isinstance(port_range, basestring):
            self.base, self.prefix = self._split_prefix(port_range)
        # Normalize prefix value
        if self.prefix is None:
            self.prefix = self.port_lenght
        # Validates base and prefix values
        if not self.base or self.base < self.port_min or \
                self.base > self.port_max:
            raise ValueError("Invalid port base.")
        if not self.prefix or self.prefix < 1 or \
                self.prefix > self.port_lenght:
            raise ValueError("Invalid CIDR-like prefix.")
        # Enable rigorous rules
        if strict:
            # Disallow offsets
            if self.prefix != self.port_lenght and \
                    not self._is_power_of_two(self.base):
                raise ValueError("Port base is not a power of Two.")
            # Disallow overflowing CIDR
            if self._raw_upper_bound() > self.port_max:
                raise ValueError("Overflowing upper bound.")

    def __repr__(self):
        return '{}(base={!r}, prefix={!r}, mask={!r})'.format(
            self.__class__.__name__, self.base, self.prefix, self.mask)

    def __str__(self):
        return '{}/{}'.format(self.base, self.prefix)

    def _is_power_of_two(self, value):
        """ Helper to check if a value is a power of 2. """
        return math.log(value, 2) % 1 == 0

    def _nearest_power_of_two(self, value):
        """ Returns nearsest power of 2. """
        return int(2 ** math.floor(math.log(value, 2)))

    def _split_prefix(self, port):
        """ Split a port range string and extract port base and CIDR prefix.

        Always returns a list of 2 integer. Defaults elements values to None.
        """
        elements = list(itertools.imap(int, port.split('/', 2)))
        elements += [None, None]
        return elements[:2]

    @property
    def mask(self):
        """ Port range binary mask, based on CIDR-like prefix.
        """
        return self.port_lenght - self.prefix

    @property
    def offset(self):
        """ Port base offset from its nearest power of two.
        """
        return self.base - self._nearest_power_of_two(self.base)

    @property
    def lower_bound(self):
        """ Port range inclusive lower bound.
        """
        return self.base

    def _raw_upper_bound(self):
        """ Compute a raw upper bound. """
        return self.lower_bound + (2 ** self.mask) - 1

    @property
    def upper_bound(self):
        """ Port range inclusive upper bound.
        """
        upper_bound = self._raw_upper_bound()
        return upper_bound if upper_bound < self.port_max else self.port_max

    @property
    def bounds(self):
        """ Produce inclusive lower and upper bounds of the port range.
        """
        return self.lower_bound, self.upper_bound