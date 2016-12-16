# -*- coding: utf-8 -*-
#
# Copyright (c) 2014-2016 Scaleway and Contributors. All Rights Reserved.
#                         Kevin Deldycke <kdeldycke@scaleway.com>
#
# Licensed under the BSD 2-Clause License (the "License"); you may not use this
# file except in compliance with the License. You may obtain a copy of the
# License at https://opensource.org/licenses/BSD-2-Clause

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals
)

import unittest

from port_range import PortRange


class TestPortRange(unittest.TestCase):

    def test_cidr_parsing(self):
        self.assertEqual(PortRange('1027/15').bounds, (1027, 1028))
        self.assertEqual(PortRange(' 1027 / 15 ').bounds, (1027, 1028))

    def test_range_parsing(self):
        # Normal range.
        self.assertEqual(PortRange('42-4242').bounds, (42, 4242))
        self.assertEqual(PortRange([42, 4242]).bounds, (42, 4242))
        self.assertEqual(PortRange(['42', '4242']).bounds, (42, 4242))

        # Single port.
        self.assertEqual(PortRange('42').bounds, (42, 42))
        self.assertEqual(PortRange(42).bounds, (42, 42))
        self.assertEqual(PortRange([42]).bounds, (42, 42))
        self.assertEqual(PortRange(['42']).bounds, (42, 42))

        # Reversed order.
        self.assertEqual(PortRange('4242-42').bounds, (42, 4242))
        self.assertEqual(PortRange([4242, 42]).bounds, (42, 4242))
        self.assertEqual(PortRange((4242, 42)).bounds, (42, 4242))
        self.assertEqual(PortRange(('4242', '42')).bounds, (42, 4242))
        self.assertEqual(PortRange(set([4242, 42])).bounds, (42, 4242))
        self.assertEqual(PortRange(set(['4242', '42'])).bounds, (42, 4242))

        # Invalid types and lenght.
        self.assertRaises(ValueError, PortRange, [None, 42])
        self.assertRaises(ValueError, PortRange, [42, None])
        self.assertRaises(ValueError, PortRange, [42, 32, 3])
        self.assertRaises(ValueError, PortRange, [42, None, 32, 3, -4])

    def test_strict_range_parsing(self):
        # Normal range.
        self.assertEqual(
            PortRange('42-4242', strict=True).bounds, (42, 4242))
        self.assertEqual(
            PortRange([42, 4242], strict=True).bounds, (42, 4242))
        self.assertEqual(
            PortRange(['42', '4242'], strict=True).bounds, (42, 4242))

        # Single port.
        self.assertEqual(PortRange('42', strict=True).bounds, (42, 42))
        self.assertEqual(PortRange(42, strict=True).bounds, (42, 42))
        self.assertEqual(PortRange([42], strict=True).bounds, (42, 42))
        self.assertEqual(PortRange(['42'], strict=True).bounds, (42, 42))

        # Reversed order.
        self.assertRaises(ValueError, PortRange, [4242, 42], True)
        self.assertRaises(ValueError, PortRange, '4242-42', True)
        self.assertRaises(ValueError, PortRange, (4242, 42), True)
        self.assertRaises(ValueError, PortRange, ('4242', '42'), True)
        # Casting a set to a list might ends up with a naturally sorted list.
        # self.assertRaises(ValueError, PortRange, set([4242, 42]), True)
        # self.assertRaises(ValueError, PortRange, set(['4242', '42']), True)

        # Invalid types and lenght.
        self.assertRaises(ValueError, PortRange, [None, 42], True)
        self.assertRaises(ValueError, PortRange, [42, None], True)
        self.assertRaises(ValueError, PortRange, [42, 32, 3], True)
        self.assertRaises(ValueError, PortRange, [42, None, 32, 3, -4], True)

    def test_cidr_properties(self):
        port = PortRange('1027/15')
        self.assertEqual(port.base, 1027)
        self.assertEqual(port.prefix, 15)
        self.assertEqual(port.cidr, (1027, 15))
        self.assertEqual(port.mask, 1)
        self.assertEqual(port.offset, 3)
        self.assertEqual(port.port_from, 1027)
        self.assertEqual(port.port_to, 1028)
        self.assertEqual(port.bounds, (1027, 1028))

    def test_range_properties(self):
        port = PortRange([4242, 42])
        self.assertEqual(str(port), '42-4242')
        self.assertEqual(port.base, 42)
        self.assertEqual(port.prefix, None)
        self.assertEqual(port.cidr, (42, None))
        self.assertEqual(port.mask, None)
        self.assertEqual(port.offset, 10)
        self.assertEqual(port.port_from, 42)
        self.assertEqual(port.port_to, 4242)
        self.assertEqual(port.bounds, (42, 4242))

    def test_normalization(self):
        port = PortRange(' 0001234 ')
        self.assertEqual(str(port), '1234')
        self.assertEqual(port.base, 1234)
        self.assertEqual(port.prefix, 16)
        self.assertEqual(port.cidr, (1234, 16))
        self.assertEqual(port.mask, 0)
        self.assertEqual(port.offset, 210)
        self.assertEqual(port.port_from, 1234)
        self.assertEqual(port.port_to, 1234)
        self.assertEqual(port.bounds, (1234, 1234))

        # Upper-bound cap.
        self.assertEqual(PortRange('64666/3').bounds, (64666, 65535))

    def test_output_string(self):
        self.assertEqual(str(PortRange('1027/15')), '1027/15')
        self.assertEqual(str(PortRange([42, 4242])), '42-4242')
        self.assertEqual(str(PortRange(42)), '42')
        self.assertEqual(str(PortRange([1027, 1028])), '1027/15')

        self.assertEqual(
            repr(PortRange([1027, 1028])),
            "PortRange(port_from=1027, port_to=1028, base=1027, offset=3, "
            "prefix=15, mask=1, is_single_port=False, is_cidr=True)")

    def test_cidr_string_rendering(self):
        self.assertEqual(PortRange([32768, 65535]).cidr_string, '32768/1')
        self.assertEqual(PortRange([32767, 65534]).cidr_string, '32767/1')
        with self.assertRaises(ValueError):
            PortRange([32767, 65535]).cidr_string

    def test_validation(self):
        # Test empty params
        self.assertRaises(ValueError, PortRange, None)
        self.assertRaises(ValueError, PortRange, [None])
        self.assertRaises(ValueError, PortRange, [None, None])

        # Invalid int
        self.assertRaises(ValueError, PortRange, ' A233 ')
        self.assertRaises(ValueError, PortRange, '1 2 3 4')
        self.assertRaises(ValueError, PortRange, 'abcd')

        # Test negative values
        self.assertRaises(ValueError, PortRange, '-24')
        self.assertRaises(ValueError, PortRange, '-24/3')
        self.assertRaises(ValueError, PortRange, '1024/-3')
        self.assertRaises(ValueError, PortRange, '-1000/-3')
        self.assertRaises(ValueError, PortRange, '-3/-1000')
        self.assertRaises(ValueError, PortRange, ' - 24')
        self.assertRaises(ValueError, PortRange, ' - 24 / 3')
        self.assertRaises(ValueError, PortRange, ' 1024 / - 3')
        self.assertRaises(ValueError, PortRange, ' - 1000 / -  3')
        self.assertRaises(ValueError, PortRange, ' -  3/  - 1000 ')

        # Test maximums and minimums
        self.assertRaises(ValueError, PortRange, '1024/0')
        self.assertRaises(ValueError, PortRange, '1024/17')
        self.assertRaises(ValueError, PortRange, '10-66666', strict=True)

        # Test capping.
        self.assertEqual(PortRange('0').bounds, (1, 1))
        self.assertRaises(ValueError, PortRange, '0', True)
        self.assertEqual(PortRange('66666').bounds, (65535, 65535))
        self.assertRaises(ValueError, PortRange, '66666', True)

        # Test notation
        self.assertRaises(ValueError, PortRange, '23/')
        self.assertRaises(ValueError, PortRange, '/4')
        self.assertRaises(ValueError, PortRange, '/4')
        self.assertRaises(ValueError, PortRange, '400-')
        self.assertRaises(ValueError, PortRange, '123 /  123/ 123')
        self.assertRaises(ValueError, PortRange, ' 123 - 31123- 1323')

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
