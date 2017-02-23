#!/usr/bin/env python

from MBTA import just_for_test, test2
import unittest

class TestMyFunction(unittest.TestCase):
	def test_just_for_test(self):
		self.assertEqual(just_for_test(1,1),2)

	def test_test2(self):
		self.assertEqual(test2(3,4),[3,4])

if __name__ == "__main__":
		unittest.main(exit=False)