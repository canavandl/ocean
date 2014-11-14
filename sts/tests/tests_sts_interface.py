#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Defines unit tests for :mod:`ocean.sts_interface` module.
"""

import unittest

from sts_interface import (create_sts_command, STS_INTERFACE)

__author__ = 'Luke Canavan'
__copyright__ = ''
__license__ = ''
__maintainer__ = ''
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

class TestSTS_Interface(unittest.TestCase):
    """
    Defines :func:`ocean.sts_interface.format_ocean_command` definition unit
    tests methods.
    """

    def test_create_sts_command(self):
        """
        Tests :func:`ocean.sts_interface.format_ocean_command` definition.
        """
        self.assertEqual(create_sts_command(
                            STS_INTERFACE.get('get_integration_time')),
                         '\x02\x00\x00')
        self.assertEqual(create_sts_command(
                            STS_INTERFACE.get('set_integration_time'), parameter=100000),
                         '\x01\x00\x06100000')

if __name__ == '__main__':
    unittest.main()