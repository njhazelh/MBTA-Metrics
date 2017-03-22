"""
This code will test the archiver module
"""

import unittest
import mbtaalerts.archiver

class ArchiverTest(unittest.TestCase):
    """
    This code will do tests
    """
    def test_example2(self):
        """
        Check that we can access the archiver module
        """
        self.assertEqual(1, mbtaalerts.archiver.helper_function())
