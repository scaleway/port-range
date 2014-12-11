# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import itertools


class PortRange(object):
    """ Port range with support of a CIDR-like (binary) notation.

    This implementation is quite liberal and allows port base that are not a
    power of two. In this case, the range is still a power of two but the base
    port has an offset.
    """

    # Max port lenght, in bytes
    port_lenght = 16
    # Max port range, in integers
    port_min = 1
    port_max = (2 ** port_lenght) - 1

    def __init__(self, port_range):
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

    def __repr__(self):
        return '{}(base={!r}, prefix={!r}, mask={!r})'.format(
            self.__class__.__name__, self.base, self.prefix, self.mask)

    def __str__(self):
        return '{}/{}'.format(self.base, self.prefix)

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
    def lower_bound(self):
        """ Port range inclusive lower bound.
        """
        return self.base

    @property
    def upper_bound(self):
        """ Port range inclusive upper bound.
        """
        upper_bound = self.lower_bound + (2 ** self.mask) - 1
        return upper_bound if upper_bound < self.port_max else self.port_max

    @property
    def bounds(self):
        """ Produce inclusive lower and upper bounds of the port range.
        """
        return self.lower_bound, self.upper_bound
