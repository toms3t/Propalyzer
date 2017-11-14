import requests
from .secret import Secret
import xml.etree.cElementTree as ET


class GreatSchools:
    """
    Class to create and execute the GreatSchools API call business logic.
    """

    def __init__(self, add_str, city, state, zip_code, county):
        self.xml_info = ''
        self.address_str = add_str
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.county = county
        self.url = ''
        self.error = ''

        self.greatschool_dict = {}

    def set_greatschool_url(self):
        """
        Function builds the GreatSchools API url, makes the request, and stores the xml_info for later use.
        :return: Sets self.error if issues arise during API calls
        """
        if Secret.GSCHOOL_API_KEY:
            self.url = 'https://api.greatschools.org/schools/nearby?'
            self.url += 'key={gs_key}&address={street}&city={city}&state={state}&zip={zip}&schoolType=public' \
                        '&radius=10&limit=100'.format(gs_key=Secret.GSCHOOL_API_KEY,
                                                      street=self.address_str,
                                                      city=self.city,
                                                      state=self.state,
                                                      zip=self.zip_code)
            try:
                school_data = requests.get(self.url)
            except:
                self.error = 'ConnectionError'
                return

            # TODO Need to verify no match condition
            if 'no exact match' in school_data.text:
                self.error = 'AddressNotFound'

            self.xml_info = school_data.text

        else:
            pass  # Missing secret key

    def set_xml_data(self):
        """
        Uses elementTree builtin to parse the XML. It then iterates through a static dict to fill out any necessary data
        required by the program that was contained in the xml file.

        :return:
        """
        tree = ET.fromstring(self.xml_info)
        for elem in tree.findall('school'):
            if self.county in elem.find('district').text:
                print(elem.find('name').text)

        # TODO Need to filter the returned schools by school type and distance
