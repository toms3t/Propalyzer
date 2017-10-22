import requests
import untangle
import usaddress
from .county import County
from .secret import Secret

ZWSID = Secret.ZWSID  ## REPLACE "Secret.ZWSID" WITH YOUR OWN ZWSID STRING ##


def mk_int(s):
    s = s.strip()
    return int(s) if s else 0


class ZillowSetup:
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
        self.street_address = ''
        self.city = ''
        self.state = ''
        self.zip_code = ''
        self.xml_info = ''
        self.error = ''

    def convert_address(self):
        """
        Function to take a string assumed to be a US address and parse it into the correct components

        :return:
        """

        address_parse = usaddress.tag(self.address_str)
        if address_parse[1] != 'Street Address':
            self.error = 'NotAStreetAddress'
        self.set_address_dict(address_parse[0])

    def set_address_dict(self, add_dict):
        for key in add_dict.keys():
            self.address_dict[key] = add_dict[key]

    def set_address(self):
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

        if 'no exact match' in prop_data.text:
            self.error = 'AddressNotFound'

        self.xml_info = prop_data.text

    def set_xml_data(self):
        """
        Method to parse listing details from the XML received from API Call
        :param DETAILS_XML: XML document from Zillow API Call
        :return: list of property details
        """
        xml_parse = untangle.parse(self.xml_info)
        xml_result = xml_parse.SearchResults_searchresults.response.results.result

        self.listing_url = xml_result.links.homedetails.cdata
        self.county_code = xml_result.FIPScounty.cdata
        self.sqft = xml_result.finishedSqFt.cdata
        self.lot_sqft = xml_result.lotSizeSqFt.cdata
        self.baths = xml_result.bathrooms.cdata
        self.beds = xml_result.bedrooms.cdata
        self.curr_value = mk_int(xml_result.zestimate.amount.cdata)
        self.value_low = mk_int(xml_result.zestimate.valuationRange.low.cdata)
        self.value_high = mk_int(xml_result.zestimate.valuationRange.high.cdata)
        self.rent_zest = xml_result.rentzestimate.amount.cdata
        self.rent_low = xml_result.rentzestimate.valuationRange.low.cdata
        self.rent_high = xml_result.rentzestimate.valuationRange.high.cdata
        self.year_built = xml_result.yearBuilt.cdata
        self.last_sold_date = xml_result.lastSoldDate.cdata
        self.neighborhood = xml_result.localRealEstate.cdata
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
