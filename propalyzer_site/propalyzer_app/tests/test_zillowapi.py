from django.test import TestCase
from ..zillow_api import ZillowSetup
import requests


class ZillowTest(TestCase):
	def setUp(self):
		self.addresses = [
			'3200 Ah We Wa St Miami, FL 33133',
			'7309 16th Ave NW Seattle, WA 98117',
			'1629 5th Ave W Seattle, WA 98119',
			'2349 Pacific Hts Rd #11 Honolulu, HI 96813',
			'2275 Palolo Ave #2275 Honolulu, HI 96816',
			'6570 Quail Pointe Cir N Memphis, TN 38120',
			'4367 Hodge Rd Memphis, TN 38109',
			'1335 W Stop 11 Rd Indianapolis, IN 46217',
			'2249 Kessler Blvd Dr E Indianapolis, IN 46220',
			'8120 SW 83rd St Miami, FL 33143'
		]

	def test_various_address_formats(self):
		for address in self.addresses:
			self.address_info = ZillowSetup(address)
			self.address_info.set_address()
			self.address_info.set_zillow_url()
			print(address)
			self.assertTrue(self.zillow_api_call())
			print('OK')

	def zillow_api_call(self):
		prop_data = requests.get(self.address_info.url)
		self.xml_info = prop_data.text
		s = 'Request successfully processed'
		return s in prop_data.text