import requests
from .secret import Secret
import xml.etree.cElementTree as ET


class GreatSchools:
	"""
	Class to create and execute the GreatSchools API call business logic.
	"""

	def __init__(self, add_str, city, state, zip_code, county):
		self.elem_xml = ''
		self.mid_xml = ''
		self.high_xml = ''
		self.address_str = add_str
		self.city = city
		self.state = state
		self.zip_code = zip_code
		self.county = county
		self.elem_url = ''
		self.mid_url = ''
		self.high_url = ''
		self.error = ''
		self.no_key = False
		self.elem_school = ''
		self.elem_school_score = ''
		self.mid_school = ''
		self.mid_school_score = ''
		self.high_school = ''
		self.high_school_score = ''
		self.greatschool_dict = {}

	def set_greatschool_urls(self):
		"""
		Function builds the GreatSchools API url, makes the request, and stores the xml_info for later use.
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

		else:
			self.no_key = True






	def get_greatschool_xml(self):
		"""
		Uses elementTree builtin to parse the XML. It then iterates through a static dict to fill out any necessary data
		required by the program that was contained in the xml file.

		:return:
		"""
		urls = [self.elem_url, self.mid_url, self.high_url]
		for url in urls:
			try:
				school_data = requests.get(url)
				print (school_data.text)
			except:
				self.error = 'ConnectionError'
				school_data = 'unknown'

			if 'no exact match' in school_data.text:
				self.error = 'AddressNotFound'

			if not self.error:
				if url == self.elem_url:
					self.elem_xml = school_data.text
				elif url == self.mid_url:
					self.mid_xml = school_data.text
				elif url == self.high_url:
					self.high_xml = school_data.text

		tree = ET.fromstring(self.xml_info)
		for elem in tree.findall('school'):
			try:
				self.greatschool_dict[elem.find('name').text] = (elem.find('distance').text, elem.find('gsRating').text)
			except AttributeError:
				continue
		print (self.url)
		print (self.greatschool_dict)
		for school in sorted(self.greatschool_dict.items(), key=lambda x: x[1]):
			if 'Elementary' in school[0] and not self.elem_school:
				self.elem_school = school[0]
				self.elem_school_score = school[1][1]
			elif 'Middle' in school[0] and not self.mid_school:
				self.mid_school = school[0]
				self.mid_school_score = school[1][1]
			elif 'High' in school[0] and not self.high_school:
				self.high_school = school[0]
				self.high_school_score = school[1][1]

