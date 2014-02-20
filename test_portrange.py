# -*- coding: utf-8 -*-

from __future__ import (unicode_literals, print_function, absolute_import,
                        division)

import unittest

from portrange import PortRange


class TestPortRange(unittest.TestCase):

    def test_properties(self):
        port = PortRange('1024/15')
        self.assertEqual(str(port), '1024/15')
        self.assertEqual(port.base, 1024)
        self.assertEqual(port.prefix, 15)
        self.assertEqual(port.mask, 1)
        self.assertEqual(port.lower_bound, 1024)
        self.assertEqual(port.upper_bound, 1025)
        self.assertEqual(port.bounds, (1024, 1025))

    def test_normalization(self):
        port = PortRange(' 0001234 ')
        self.assertEqual(str(port), '1234/16')
        self.assertEqual(port.base, 1234)
        self.assertEqual(port.prefix, 16)
        self.assertEqual(port.mask, 0)
        self.assertEqual(port.lower_bound, 1234)
        self.assertEqual(port.upper_bound, 1234)
        self.assertEqual(port.bounds, (1234, 1234))
        # Upper bound cap
        self.assertEqual(PortRange('64666/3').bounds, (64666, 65535))

    def test_validation(self):
        # Invalid int
        self.assertRaises(ValueError, PortRange, ' A233 ')
        # Test negative values
        self.assertRaises(ValueError, PortRange, '-24/3')
        self.assertRaises(ValueError, PortRange, '1024/-3')
        # Test maximums and minimums
        self.assertRaises(ValueError, PortRange, '1024/0')
        self.assertRaises(ValueError, PortRange, '1024/17')
        self.assertRaises(ValueError, PortRange, '66666')
        self.assertRaises(ValueError, PortRange, '0')

    def test_strict_mode(self):
        # Test power of two port base
        PortRange('257', strict=True)
        PortRange('257/16', strict=True)
        self.assertRaises(ValueError, PortRange, '257/4', strict=True)
        # Test overflowing upper bound
        self.assertRaises(ValueError, PortRange, '65535/8', strict=True)

    def test_computation(self):
        self.assertEqual(PortRange('2/3').bounds, (2, 8193))
        self.assertEqual(PortRange('7/3').bounds, (7, 8198))
