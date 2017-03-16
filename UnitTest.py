#!/usr/bin/env python

from MBTA import *
import unittest

class TestExistence(unittest.TestCase):
	"""
	def test_just_for_test(self):
		self.assertEqual(just_for_test(1,1),2)
	"""

	def test_deserveAlert(self):
		self.assertTrue(deserveAlert(100))
		self.assertTrue(deserveAlert(11))
		self.assertTrue(deserveAlert(12))
		self.assertTrue(deserveAlert(50))
		self.assertTrue(deserveAlert(100))
		self.assertTrue(deserveAlert(200))
		self.assertTrue(deserveAlert(10))
		self.assertFalse(deserveAlert(9))
		self.assertFalse(deserveAlert(0))
		self.assertFalse(deserveAlert(-1))
		self.assertFalse(deserveAlert(-10))
		self.assertFalse(deserveAlert(-100))
		self.assertFalse(deserveAlert(-10000))
		self.assertFalse(deserveAlert(-1100000))

		

	def test_isAlertExisted(self):

		# need to archive more data to wirte on this test 
		self.assertTrue(test_isAlertExisted("CR-SevereWeatherBlue-418")
		self.assertTrue(test_isAlertExisted("CR-SevereWeatherBlue-711"))
		self.assertTrue(test_isAlertExisted("CR-SevereWeatherBlue-716"))
		
		self.assertFalse(test_isAlertExisted("CR-Newburyport-CR-Weekday-Newburyport-Dec14-152"))
		self.assertFalse(test_isAlertExisted("CR-Newburyport-CR-Weekday-Newburyport-Dec14-150"))
		self.assertFalse(test_isAlertExisted("CR-Newburyport-CR-Weekday-Newburyport-Dec14-156"))
		self.assertFalse(test_isAlertExisted("CR-Newburyport-CR-Weekday-Newburyport-Dec14-165"))
		self.assertFalse(test_isAlertExisted("CR-Newburyport-CR-Weekday-Newburyport-Dec14-175"))
		self.assertFalse(test_isAlertExisted("CR-Newburyport-CR-Weekday-Newburyport-Dec14-153"))



	
class TestAccuracy(unittest.TestCase):
	def test_alertAccuracy(self):
		#Test cases for accurate
		self.assertEqual(alertAccuracy([5,15],7),"accurate")
		self.assertEqual(alertAccuracy([10,20],15),"accurate")
		self.assertEqual(alertAccuracy([15,20],15),"accurate")
		self.assertEqual(alertAccuracy([15,20],20),"accurate")

		self.assertEqual(alertAccuracy([5,15],3), "high")
		self.assertEqual(alertAccuracy([5,15],4), "high")
		self.assertEqual(alertAccuracy([5,15],1), "high")
		self.assertEqual(alertAccuracy([5,15],0), "high")
		self.assertEqual(alertAccuracy([5,15],-1), "high")
		self.assertEqual(alertAccuracy([5,15],-10), "high")


		self.assertEqual(alertAccuracy([5,15],19), "low")
		self.assertEqual(alertAccuracy([5,15],16), "low")
		self.assertEqual(alertAccuracy([5,15],30), "low")
		self.assertEqual(alertAccuracy([5,15],10000), "low")
		self.assertEqual(alertAccuracy([5,15],14000), "low")
		self.assertEqual(alertAccuracy([5,15],50000), "low")

		self.assertEqual(alertAccuracy([],-5), "no estimation")
		self.assertEqual(alertAccuracy([],0), "no estimation")
		self.assertEqual(alertAccuracy([],0), "no estimation")
		self.assertEqual(alertAccuracy([],20), "no estimation")
		self.assertEqual(alertAccuracy([],-10), "no estimation")
		self.assertEqual(alertAccuracy([],-10), "no estimation")
		




class TestTimeliness(unittest.TestCase):
	#alert sent out within 5mins of train scheduled departure
	def test_isAlertTimeliness:
		self.assertTrue(isAlertTimeliness([3,15,0,2016], [3,20,0,2016]))
		self.assertTrue(isAlertTimeliness([3,15,0,2016], [3,15,55,2016]))
		self.assertTrue(isAlertTimeliness([3,15,0,2016], [3,17,32,2016]))
		self.assertTrue(isAlertTimeliness([3,15,0,2016], [3,18,30,2016]))
		self.assertTrue(isAlertTimeliness([3,15,0,2016], [3,19,0,2016]))
		self.assertTrue(isAlertTimeliness([3,15,0,2016], [3,19,59,2016]))

		#alert sent out before the train's departure 
		self.assertTrue(isAlertTimeliness([3,15,0,2016], [3,14,0,2016]))
		self.assertTrue(isAlertTimeliness([3,15,0,2016], [3,10,55,2016]))
		self.assertTrue(isAlertTimeliness([3,15,0,2016], [3,13,32,2016]))
		self.assertTrue(isAlertTimeliness([3,15,0,2016], [3,12,30,2016]))
		self.assertTrue(isAlertTimeliness([3,15,0,2016], [3,11,0,2016]))
		self.assertTrue(isAlertTimeliness([3,15,0,2016], [3,10,59,2016]))

		#alert sent out after 5mins of train sechdueld deparutre

		self.assertFalse(isAlertTimeliness([2,15,0,2016], [3,20,0,2016]))
		self.assertFalse(isAlertTimeliness([3,5,0,2016], [3,15,55,2016]))
		self.assertFalse(isAlertTimeliness([3,5,0,2016], [3,17,32,2016]))
		self.assertFalse(isAlertTimeliness([3,15,0,2016], [3,28,30,2016]))
		self.assertFalse(isAlertTimeliness([3,15,0,2016], [3,19,0,2016]))
		self.assertFalse(isAlertTimeliness([0,15,0,2016], [3,19,59,2016]))









class TestOtherfunctions(unittest.TestCase):
	def test_convertSecondToMinute:
		self.assertEqual(convertSecondToMinute(60),1)
		self.assertEqual(convertSecondToMinute(120),2)
		self.assertEqual(convertSecondToMinute(180),3)
		self.assertEqual(convertSecondToMinute(30),0.5)
		self.assertEqual(convertSecondToMinute(5),5/60)
		self.assertEqual(convertSecondToMinute(0),0)
		self.assertEqual(convertSecondToMinute(-60),-1)
		self.assertEqual(convertSecondToMinute(-120),-2)
		self.assertEqual(convertSecondToMinute(-30),-0.5)
	







if __name__ == "__main__":
		unittest.main(exit=False)
