import re
import xml.etree.cElementTree as ET
import requests
from bs4 import BeautifulSoup
import usaddress
from .secret import Secret
from .greatschools import GreatSchools
from .county import County


ZWSID = Secret.ZWSID


def mk_int(s):
    """
    Function to change a string to int or 0 if None.

    :param s: String to change to int.
    :return: Either returns the int of the string or 0 for None.
    """
    try:
        s = s.strip()
        return int(s) if s else 0
    except:
        return s


class PropSetup:
    """
    Class to create property objects and execute the Zillow API call business logic.
    """

    def __init__(self, add_str):
        self.address = add_str
        self.address_dict = {
            'AddressNumber': 0,
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
            'ZipCode': ''
        }

        self.zillow_dict = {
            'homedetails': '',
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
            'localRealEstate': '',
            'address/latitude': '',
            'address/longitude': ''
        }

        self.areavibes_dict = {
            'crime': '',
            'livability': '',
            'cost_of_living': '',
            'housing': '',
            'schools': '',
            'weather': '',
            'employment': ''
        }
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
        self.rent = 0
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
        self.lat = ''
        self.long = ''
        self.taxes = 0
        self.hoa = 0
        self.vacancy = 0.0
        self.vacancy_rate = 0.0
        self.oper_income = 0
        self.down_payment_percentage = 0.0
        self.down_payment = 0
        self.init_cash_invest = 0
        self.oper_exp = 0
        self.net_oper_income = 0
        self.initial_market_value = 0
        self.interest_rate = 0.0
        self.mort_payment = 0
        self.total_mortgage = 0
        self.closing_costs = 0
        self.initial_improvements = 0
        self.cost_per_sqft = 0
        self.insurance = 0
        self.maintenance = 0
        self.prop_management_fee = 0
        self.utilities = 0
        self.tenant_placement_fee = 0
        self.resign_fee = 0
        self.notes = ''
        self.pub_date = ''
        self.rtv = 0.0
        self.cash_flow = 0
        self.oper_exp_ratio = 0.0
        self.debt_cover_ratio = 0.0
        self.cash_on_cash_return = 0.0
        self.cap_rate = 0.0
        self.schools = ''
        self.school_scores = ''
        self.county = ''
        self.disaster_dict = {}

        try:
            self.prop_management_fee = int(.09 * int(self.rent))
        except ValueError:
            self.prop_management_fee = 0
        self.initial_market_value = self.curr_value
        self.initial_improvements = 0
        self.insurance = 1000
        self.maintenance = 800
        self.taxes = 1500
        self.hoa = 0
        self.utilities = 0
        self.interest_rate = 4.75
        self.down_payment_percentage = 25
        self.down_payment = int(self.curr_value) * \
            (self.down_payment_percentage / 100.0)
        self.closing_costs = int(.03 * int(self.curr_value))

    def get_info(self):
        self.set_address()
        self.set_zillow_url()
        self.set_xml_data()
        self.set_areavibes_info()
        self.set_disaster_info()
        self.schools = GreatSchools(
            self.address, self.city, self.state, self.zip_code, self.county)
        self.schools.set_greatschool_urls()
        if self.schools.api_key and self.schools.DAILY_API_CALL_COUNT <= 2950:
            for url in self.schools.urls:
                self.schools.get_greatschool_xml(url)

        else:
            self.schools.elem_school = 'Unknown'
            self.schools.mid_school = 'Unknown'
            self.schools.high_school = 'Unknown'
        self.schools = dict((key, value) for (key, value) in self.schools.__dict__.items())

    def dict_from_class(self):

        return dict((key, value) for (key, value) in self.__dict__.items())

    def __convert_address(self):
        """
        Function to take a string assumed to be a US address and parse it into the correct components.

        :return: Uses self.error to notify requester if an error occurred.
        """

        address_parse = usaddress.tag(self.address)
        if address_parse[1] != 'Street Address':
            self.error = 'NotAStreetAddress'
        self.__set_address_dict(address_parse[0])

    def __set_address_dict(self, add_dict):
        """
        Takes the parameters if the untangled address and fills out the address dict for later usage.
        :param add_dict: Parsed US address dictionary
        :return: None. Just sets the class obj address_dict
        """
        for key in add_dict.keys():
            self.address_dict[key] = add_dict[key]

    def set_address(self):
        """
        Main function call to convert a string to an US address and generates necessary parameters to be used later.
        :return:
        """
        self.__convert_address()
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
        self.lot_sqft = mk_int(self.zillow_dict['lotSizeSqFt'])
        self.baths = self.zillow_dict['bathrooms']
        self.beds = mk_int(self.zillow_dict['bedrooms'])
        self.curr_value = mk_int(self.zillow_dict['zestimate/amount'])
        self.value_low = mk_int(
            self.zillow_dict['zestimate/valuationRange/low'])
        self.value_high = mk_int(
            self.zillow_dict['zestimate/valuationRange/high'])
        self.rent = mk_int(self.zillow_dict['rentzestimate/amount'])
        self.rent_low = mk_int(
            self.zillow_dict['rentzestimate/valuationRange/low'])
        self.rent_high = mk_int(
            self.zillow_dict['rentzestimate/valuationRange/high'])
        self.year_built = mk_int(self.zillow_dict['yearBuilt'])
        self.last_sold_date = self.zillow_dict['lastSoldDate']
        self.neighborhood = self.zillow_dict['localRealEstate']
        self.county = County.county_finder(self.county_code)
        self.lat = self.zillow_dict['address/latitude']
        self.long = self.zillow_dict['address/longitude']

    def set_areavibes_url(self):
        """
        Method that returns formatted areavibes URL for data retrieval
        :return: Returns URL used to obtain areavibes data
        """
        areavibes_url1 = 'http://www.areavibes.com/{}-{}/livability/'.format(
            self.address_dict['PlaceName'],
            self.address_dict['StateName'])
        areavibes_url2 = '?addr={}+{}+{}+{}&ll={}+{}'.format(
            self.address_dict['AddressNumber'],
            self.address_dict['StreetNamePreDirectional'],
            self.address_dict['StreetName'],
            self.address_dict['StreetNamePostType'],
            self.lat, self.long)
        areavibes_url = areavibes_url1 + areavibes_url2
        return areavibes_url

    def set_areavibes_info(self):
        """
        Method that generates the areavibes dictionary with areavibes information for a given address.
        :return: areavibes_dict - Dictionary that contains ratings sourced from areavibes.com based on a given address
        for the following categories:
            - Livability
            - Crime
            - Cost of Living
            - schools
            - Employment
            - Housing
            - Weather
        """
        url = self.set_areavibes_url()
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        info_block = soup.find_all('nav', class_='category-menu')
        try:
            result_string = info_block[0].get_text()
        except IndexError:
            result_string = 'Unknown'

        parsed = ''
        livability = ''
        cost_of_living = ''
        crime = ''
        employment = ''
        housing = ''
        schools = ''
        weather = ''

        try:
            parsed = re.search(
                'Livability(.*?)'
                'Amenities(.*?)'
                'Cost of Living(.*?)'
                'Crime(.*?)'
                'Employment(.*?)'
                'Housing(.*?)'
                'Schools(.*?)'
                'Weather(.*?)$', result_string)
        except AttributeError:
            livability = 'Unknown'
            cost_of_living = 'Unknown'
            crime = 'Unknown'
            employment = 'Unknown'
            housing = 'Unknown'
            schools = 'Unknown'
            weather = 'Unknown'
        if parsed:
            try:
                livability = parsed.group(1)
            except IndexError:
                livability = 'Unknown'
            try:
                cost_of_living = parsed.group(3)
            except IndexError:
                cost_of_living = 'Unknown'
            try:
                crime = parsed.group(4)
            except IndexError:
                crime = 'Unknown'
            try:
                employment = parsed.group(5)
            except IndexError:
                employment = 'Unknown'
            try:
                housing = parsed.group(6)
            except IndexError:
                housing = 'Unknown'
            try:
                schools = parsed.group(7)
            except IndexError:
                schools = 'Unknown'
            try:
                weather = parsed.group(8)
            except IndexError:
                weather = 'Unknown'
        self.areavibes_dict = {
            'livability': livability,
            'crime': crime,
            'cost_of_living': cost_of_living,
            'schools': schools,
            'employment': employment,
            'housing': housing,
            'weather': weather
        }

    def set_disaster_info(self):
        """
        Method that generates the self.disaster_dict dictionary which includes the last 5 disasters from fema.gov for
        the county of the property being researched. The dictionary includes disaster type, date, county, state, url,
        and fema id for each disaster.
        """
        local_disasters = []
        disaster_dict = {}
        if 'County' in self.county:
            county_pattern = re.search('^(.*?) County', self.county)
            try:
                county = county_pattern.group(1)
            except AttributeError:
                county = self.county
        else:
            county = self.county
        url1 = 'https://www.fema.gov/api/open/v1/DisasterDeclarationsSummaries?'
        url2 = "$filter=state eq '{}'&$select=state, incidentType, declaredCountyArea, title, ".format(
            self.state.upper())
        url3 = 'incidentEndDate&$orderby=incidentEndDate'
        url = url1+url2+url3
        resp = requests.get(url)
        resp_json = resp.json()
        for dis in resp_json['DisasterDeclarationsSummaries']:
            if county in dis['declaredCountyArea']:
                local_disasters.append(dis)
        last_5_disasters = local_disasters[-5:]
        c = 1
        if not last_5_disasters:
            disaster_dict[1] = ['No Records Found',
                                'NA', 'NA', 'NA', 'NA', 'NA']
            disaster_dict[2] = ['No Records Found',
                                'NA', 'NA', 'NA', 'NA', 'NA']
            disaster_dict[3] = ['No Records Found',
                                'NA', 'NA', 'NA', 'NA', 'NA']
            disaster_dict[4] = ['No Records Found',
                                'NA', 'NA', 'NA', 'NA', 'NA']
            disaster_dict[5] = ['No Records Found',
                                'NA', 'NA', 'NA', 'NA', 'NA']
        else:
            for disaster in last_5_disasters[::-1]:
                disaster_dict[c] = [
                    disaster['incidentType'],
                    disaster['incidentEndDate'][:10],
                    disaster['declaredCountyArea'],
                    disaster['state'],
                    url1[:-1]+'/'+disaster['id'],
                    disaster['title']
                ]
                c += 1
            if not disaster_dict[2]:
                disaster_dict[2] = ['No Records Found',
                                    'NA', 'NA', 'NA', 'NA', 'NA']
            if not disaster_dict[3]:
                disaster_dict[3] = ['No Records Found',
                                    'NA', 'NA', 'NA', 'NA', 'NA']
            if not disaster_dict[4]:
                disaster_dict[4] = ['No Records Found',
                                    'NA', 'NA', 'NA', 'NA', 'NA']
            if not disaster_dict[5]:
                disaster_dict[5] = ['No Records Found',
                                    'NA', 'NA', 'NA', 'NA', 'NA']

        self.disaster_dict = disaster_dict

    @property
    def __str__(self):
        return self.address
