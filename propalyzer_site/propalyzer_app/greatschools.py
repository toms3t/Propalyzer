import requests
import logging
from .secret import Secret
import xml.etree.cElementTree as ET

LOG = logging.getLogger(__name__)


class GreatSchools:

	DAILY_API_CALL_COUNT = 0

	"""
	Class to create and execute the GreatSchools API call logic with the goal of retrieving the elementary,
	middle, and high schools that are nearest to the property address.
	"""

	def __init__(self, add_str, city, state, zip_code, county):
		self.address_str = add_str
		self.city = city
		self.state = state
		self.zip_code = zip_code
		self.county = county
		self.elem_url = ''
		self.mid_url = ''
		self.high_url = ''
		self.urls = []
		self.api_key = True
		self.error = ''
		self.elem_school = ''
		self.elem_school_score = ''
		self.mid_school = ''
		self.mid_school_score = ''
		self.high_school = ''
		self.high_school_score = ''

	def set_greatschool_urls(self):
		"""
		Function builds the GreatSchools API URLs (one for each level of school)
		:return: Sets self.error if issues arise during API calls
		"""
		if Secret.GSCHOOL_API_KEY:
			self.elem_url = 'https://api.greatschools.org/schools/nearby?'
			self.elem_url += 'key={gs_key}&address={street}&city={city}&state={state}&zip={zip}&schoolType=public' \
				'&radius=5&limit=2&levelCode={level}'.format(
													gs_key=Secret.GSCHOOL_API_KEY,
													street=self.address_str,
													city=self.city,
													state=self.state,
													zip=self.zip_code,
													level='elementary-schools')
			self.mid_url = self.elem_url.replace('elementary-schools', 'middle-schools')
			self.high_url = self.elem_url.replace('elementary-schools', 'high-schools')
			self.urls = [self.elem_url, self.mid_url, self.high_url]
		else:
			self.api_key = False

	def get_greatschool_xml(self, url):
		"""
		Uses elementTree builtin to parse the XML. It then generates a dictionary of key/value pairs found in the
		XML, including school name, distance from property address, and GreatSchools.org rating. The elementary,
		middle, and high schools closest to the given property address are populated as attributes of the
		GreatSchools object.
		:param: Url used for GreatSchools API call for XML retrieval
		:return: None

		"""
		if self.api_key:
			dist = 20
			school_name = ''
			school_score = ''
			greatschools_dict = {}
			school_data = ''

			try:
				school_data = requests.get(url)
				GreatSchools.DAILY_API_CALL_COUNT += 1
				LOG.debug('Greatschools API CALL COUNT --- {}'.format(GreatSchools.DAILY_API_CALL_COUNT))
			except:
				LOG.debug('Greatschools ConnectionError --- Tried URL - {}'.format(url))
				self.error = 'ConnectionError'

			if 'no exact match' in school_data.text:
				LOG.debug('Greatschools --- No exact match - {}'.format(url))
				self.error = 'NoExactMatch'

			if not self.error:
				school_xml = school_data.text

				tree = ET.fromstring(school_xml)
				for elem in tree.findall('school'):
					try:
						greatschools_dict[elem.find('name').text] = (elem.find('distance').text, elem.find('gsRating').text)
					except AttributeError:
						continue
				for school in sorted(greatschools_dict.items(), key=lambda x: x[1]):
					if float(school[1][0]) < dist:
						dist = float(school[1][0])
						school_name = school[0]
						school_score = school[1][1]
				if url == self.elem_url:
					self.elem_school = school_name
					self.elem_school_score = school_score
				if url == self.mid_url:
					self.mid_school = school_name
					self.mid_school_score = school_score
				if url == self.high_url:
					self.high_school = school_name
					self.high_school_score = school_score
			else:
				self.elem_school = 'Unknown'
				self.elem_school_score = 'Unknown'
				self.mid_school = 'Unknown'
				self.mid_school_score = 'Unknown'
				self.high_school = 'Unknown'
				self.high_school_score = 'Unknown'
