import requests
import usaddress
from .county import County
from .secret import Secret
import xml.etree.cElementTree as ET

ZWSID = Secret.ZWSID  ## REPLACE "Secret.ZWSID" WITH YOUR OWN ZWSID STRING ##


def mk_int(s):
    """
    Function to change a string to int or 0 if None.

    :param s: String to change to int.
    :return: Either returns the int of the string or 0 for None.
    """
    s = s.strip()
    return int(s) if s else 0


class ZillowSetup:
    """
    Class to create and execute the Zillow API call business logic.
    """
    def __init__(self, add_str):
        self.address_str = add_str
        self.address_dict = {'AddressNumber': 0,
                             'AddressNumberPrefix': '',
                             'AddressNumberSuffix': '',
                             'BuildingName': '',
                             'CornerOf': '',
                             'IntersectionSeparator': '',
                             'LandmarkName': '',
                             'NotAddress': '',
                             'OccupancyType': '',
                             'OccupancyIdentifier': '',
                             'PlaceName': '',
                             'Recipient': '',
                             'StateName': '',
                             'StreetName': '',
                             'StreetNamePreDirectional': '',
                             'StreetNamePreModifier': '',
                             'StreetNamePreType': '',
                             'StreetNamePostDirectional': '',
                             'StreetNamePostModifier': '',
                             'StreetNamePostType': '',
                             'SubaddressIdentifier': '',
                             'SubaddressType': '',
                             'USPSBoxGroupID': '',
                             'USPSBoxGroupType': '',
                             'USPSBoxID': '',
                             'USPSBoxType': '',
                             'ZipCode': ''}

        self.zillow_dict = {'homedetails': '',
                            'FIPScounty': '',
                            'finishedSqFt': '',
                            'lotSizeSqFt': '',
                            'bathrooms': '',
                            'bedrooms': '',
                            'zestimate/amount': '',
                            'zestimate/valuationRange/low': '',
                            'zestimate/valuationRange/high': '',
                            'rentzestimate/amount': '',
                            'rentzestimate/valuationRange/low': '',
                            'rentzestimate/valuationRange/high': '',
                            'yearBuilt': '',
                            'lastSoldDate': '',
                            'localRealEstate': ''}

        self.street_address = ''
        self.city = ''
        self.state = ''
        self.zip_code = 0
        self.listing_url = ''
        self.county_code = 0
        self.sqft = 0
        self.lot_sqft = 0
        self.baths = 0
        self.beds = 0
        self.curr_value = 0
        self.value_low = 0
        self.value_high = 0
        self.rent_zest = 0
        self.rent_low = 0
        self.rent_high = 0
        self.year_built = 0
        self.last_sold_date = ''
        self.neighborhood = ''
        self.county = ''
        self.listing_details = ''
        self.xml_info = ''
        self.url = ''
        self.error = ''

    def convert_address(self):
        """
        Function to take a string assumed to be a US address and parse it into the correct components.

        :return: Uses self.error to notify requester if an error occurred.
        """

        address_parse = usaddress.tag(self.address_str)
        if address_parse[1] != 'Street Address':
            self.error = 'NotAStreetAddress'
        self.set_address_dict(address_parse[0])

    def set_address_dict(self, add_dict):
        """
        Takes the parameters if the untangled address and fills out the address dict for later usage.
        :param add_dict: Parsed US address dictionary
        :return: None. Just sets the class obj address_dict
        """
        for key in add_dict.keys():
            self.address_dict[key] = add_dict[key]

    def set_address(self):
        """
        Mian function call to convert a string to an US address and generates necessary parameters to be used later.
        :return:
        """
        self.convert_address()
        self.street_address = (str(self.address_dict['AddressNumberPrefix']) + ' ' +
                               str(self.address_dict['AddressNumber']) + ' ' +
                               str(self.address_dict['AddressNumberSuffix']) + ' ' +
                               str(self.address_dict['StreetNamePreDirectional']) + ' ' +
                               str(self.address_dict['StreetName']) + ' ' +
                               str(self.address_dict['StreetNamePostDirectional']) + ' ' +
                               str(self.address_dict['StreetNamePostType']))

        self.city = self.address_dict['PlaceName']
        self.state = self.address_dict['StateName']
        self.zip_code = self.address_dict['ZipCode']

    def set_zillow_url(self):
        """
        Function builds the Zillow API url, makes the request, and stores the xml_info for later use.
        :return: Sets self.error if issues arise during API calls
        """
        self.url = 'http://www.zillow.com/webservice/GetDeepSearchResults.htm?'
        self.url += 'zws-id={ZWSID}&address={street}&citystatezip={city}%2C+{state}+{zip}&' \
                    'rentzestimate=true'.format(ZWSID=ZWSID,
                                                street=self.street_address,
                                                city=self.city,
                                                state=self.state,
                                                zip=self.zip_code)

        try:
            prop_data = requests.get(self.url)
        except:
            self.error = 'ConnectionError'
            return

        if 'no exact match' in prop_data.text:
            self.error = 'AddressNotFound'

        self.xml_info = prop_data.text

    def set_xml_data(self):
        """
        Uses elementTree builtin to parse the XML. It then iterates through a static dict to fill out any necessary data
        required by the program that was contained in the xml file.

        Not sure if listing_details is necessary, but left in since it was part of previous logic
        :return:
        """
        tree = ET.fromstring(self.xml_info)
        for tag in self.zillow_dict.keys():
            for elem in tree.findall('.//' + tag):
                if elem.text is not None:
                    self.zillow_dict[tag] = elem.text

        self.listing_url = self.zillow_dict['homedetails']
        self.county_code = self.zillow_dict['FIPScounty']
        self.sqft = self.zillow_dict['finishedSqFt']
        self.lot_sqft = self.zillow_dict['lotSizeSqFt']
        self.baths = self.zillow_dict['bathrooms']
        self.beds = self.zillow_dict['bedrooms']
        self.curr_value = mk_int(self.zillow_dict['zestimate/amount'])
        self.value_low = mk_int(self.zillow_dict['zestimate/valuationRange/low'])
        self.value_high = mk_int(self.zillow_dict['zestimate/valuationRange/high'])
        self.rent_zest = self.zillow_dict['rentzestimate/amount']
        self.rent_low = self.zillow_dict['rentzestimate/valuationRange/low']
        self.rent_high = self.zillow_dict['rentzestimate/valuationRange/high']
        self.year_built = self.zillow_dict['yearBuilt']
        self.last_sold_date = self.zillow_dict['lastSoldDate']
        self.neighborhood = self.zillow_dict['localRealEstate']
        self.county = County.county_finder(self.county_code)

        self.listing_details = [
            self.listing_url,
            self.county_code,
            self.sqft,
            self.lot_sqft,
            self.baths,
            self.beds,
            self.curr_value,
            self.value_low,
            self.value_high,
            self.rent_zest,
            self.rent_low,
            self.rent_high,
            self.year_built,
            self.last_sold_date,
            self.neighborhood
        ]