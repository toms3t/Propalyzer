import requests
import re
from django.utils import timezone
from decimal import Decimal, getcontext
from bs4 import BeautifulSoup
import usaddress
from .county import County
from .secret import Secret
import xml.etree.cElementTree as ET

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
            'education': '',
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

    def create_test_obj(self):
        """
        Method to create test PropSetup instance for use by 'test_property.py'
        :return: Sets object attributes -- does not return an object
        """
        self.address = '3465-N-Main-St-Soquel-CA-95073'
        self.listing_url = 'http://www.zillow.com/homedetails/3465-N-Main-St-Soquel-CA-95073/16128477_zpid/'
        self.neighborhood = 'Unknown'
        self.pub_date = timezone.now()
        self.curr_value = 699600
        self.value_low = 680101
        self.value_high = 751691
        self.initial_market_value = 699600
        self.initial_improvements = 5000
        self.rent = 2600
        self.rent_low = 2106
        self.rent_high = 2990
        self.sqft = 1058
        self.lot_sqft = 20343
        self.beds = 2
        self.baths = 1.5
        self.year_built = 1950
        self.hoa = 100
        self.maintenance = 800
        self.tenant_placement_fee = 500
        self.taxes = 2000
        self.utilities = 30
        self.insurance = 1000
        self.prop_management_fee = 234
        self.resign_fee = 300
        self.vacancy_rate = 0.08
        self.notes = ''
        self.interest_rate = 4.75
        self.down_payment_percentage = 25.00
        self.schools = ''
        self.school_scores = ''
        self.county = 'Santa Cruz County'
        self.cost_per_sqft = self.cost_per_sqft_calc
        self.down_payment = self.down_payment_calc
        self.vacancy = self.vacancy_calc
        self.closing_costs = self.closing_costs_calc
        self.oper_income = self.oper_inc_calc
        self.oper_exp = self.oper_exp_calc
        self.net_oper_income = self.net_oper_income_calc
        self.total_mortgage = self.total_mortgage_calc
        self.mort_payment = self.mort_payment_calc
        self.cash_flow = self.cash_flow_calc
        self.oper_exp_ratio = self.oper_exp_ratio_calc
        self.debt_cover_ratio = self.debt_coverage_ratio_calc
        self.rtv = self.rtv_calc
        self.init_cash_invest = self.init_cash_invested_calc
        self.cap_rate = self.cap_rate_calc
        self.cash_on_cash_return = self.cash_on_cash_calc

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
        Mian function call to convert a string to an US address and generates necessary parameters to be used later.
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
        self.value_low = mk_int(self.zillow_dict['zestimate/valuationRange/low'])
        self.value_high = mk_int(self.zillow_dict['zestimate/valuationRange/high'])
        self.rent = mk_int(self.zillow_dict['rentzestimate/amount'])
        self.rent_low = mk_int(self.zillow_dict['rentzestimate/valuationRange/low'])
        self.rent_high = mk_int(self.zillow_dict['rentzestimate/valuationRange/high'])
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
        :param ADDRESSDICT: Identified components of the property address (i.e. street name, city, zip code, etc.)
        :return: areavibes_dict - Dictionary that contains ratings sourced from areavibes.com based on a given address
        for the following categories:
            - Livability
            - Crime
            - Cost of Living
            - Education
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
        try:
            livability = int(re.findall('Livability(\d+)', result_string)[0])
        except IndexError:
            livability = 0
        try:
            crime = re.findall('Crime(.*?)Edu', result_string)[0]
        except IndexError:
            crime = 'Unknown'
        try:
            cost_of_living = re.findall('Living(.*?)Crime', result_string)[0]
        except IndexError:
            cost_of_living = 'Unknown'
        try:
            education = re.findall('Education(.*?)Empl', result_string)[0]
        except IndexError:
            education = 'Unknown'
        try:
            employment = re.findall('Employment(.*?)Hou', result_string)[0]
        except IndexError:
            employment = 'Unknown'
        try:
            housing = re.findall('Housing(.*?)Weather', result_string)[0]
        except IndexError:
            housing = 'Unknown'
        try:
            weather = re.findall('Weather(.*)$', result_string)[0].rstrip()
        except IndexError:
            weather = 'Unknown'
        self.areavibes_dict = {
            'livability': livability,
            'crime': crime,
            'cost_of_living': cost_of_living,
            'education': education,
            'employment': employment,
            'housing': housing,
            'weather': weather
        }

    @property
    def __str__(self):
        return self.address

    @property
    def oper_inc_calc(self):
        self.oper_income = int(mk_int(self.rent) - self.vacancy)
        return self.oper_income

    @property
    def init_cash_invested_calc(self):
        self.down_payment = self.down_payment_calc
        self.init_cash_invest = int(self.down_payment + mk_int(self.closing_costs) + mk_int(self.initial_improvements))
        return self.init_cash_invest

    @property
    def vacancy_calc(self):
        self.vacancy_rate = .08
        self.vacancy = int(self.vacancy_rate * mk_int(self.rent))
        return self.vacancy

    @property
    def oper_exp_calc(self):
        self.oper_exp = int((
                (mk_int(self.resign_fee) / 12) +
                (mk_int(self.taxes) / 12) +
                (mk_int(self.hoa) / 12) +
                mk_int(self.utilities) +
                mk_int(self.prop_management_fee) +
                (mk_int(self.insurance) / 12) +
                (mk_int(self.maintenance) / 12) +
                (mk_int(self.tenant_placement_fee) / 12)
        )
        )
        return self.oper_exp

    @property
    def net_oper_income_calc(self):
        self.net_oper_income = int(self.oper_income - self.oper_exp)
        return self.net_oper_income

    @property
    def cash_flow_calc(self):
        self.cash_flow = int(self.net_oper_income - self.mort_payment)
        return self.cash_flow

    @property
    def oper_exp_ratio_calc(self):
        getcontext().prec = 2
        try:
            self.oper_exp_ratio = float(Decimal(self.oper_exp) / Decimal(self.oper_income))
        except ZeroDivisionError:
            self.oper_exp_ratio = 0.00
        self.oper_exp_ratio = self.oper_exp_ratio + 0
        return self.oper_exp_ratio

    @property
    def debt_coverage_ratio_calc(self):
        getcontext().prec = 2
        if self.mort_payment:
            try:
                self.debt_cover_ratio = float(Decimal(self.net_oper_income) / Decimal(self.mort_payment))
            except ZeroDivisionError:
                self.debt_cover_ratio = 0.00
            return self.debt_cover_ratio
        else:
            return None

    @property
    def cap_rate_calc(self):
        getcontext().prec = 2
        self.initial_market_value = mk_int(self.curr_value)
        try:
            self.cap_rate = float(Decimal((self.net_oper_income * 12) / Decimal(self.initial_market_value)))
        except ZeroDivisionError:
            self.cap_rate = 0.00
        self.cap_rate = self.cap_rate + 0
        return self.cap_rate

    @property
    def cash_on_cash_calc(self):
        getcontext().prec = 3
        try:
            self.cash_on_cash_return = float(Decimal((self.cash_flow * 12) / Decimal(self.init_cash_invest)))
        except ZeroDivisionError:
            self.cash_on_cash_return = 0.00
        return self.cash_on_cash_return

    @property
    def down_payment_calc(self):
        self.down_payment = int((float(self.down_payment_percentage) * mk_int(self.curr_value)) / 100)
        return self.down_payment

    @property
    def total_mortgage_calc(self):
        getcontext().prec = 8
        self.total_mortgage = mk_int(self.curr_value) - self.down_payment
        return int(self.total_mortgage)

    @property
    def mort_payment_calc(self):
        i = (float(self.interest_rate) / 100) / 12
        n = 360
        p = self.total_mortgage
        self.mort_payment = int(p * (i * (1 + i) ** n) / ((1 + i) ** n - 1))
        return self.mort_payment

    @property
    def cost_per_sqft_calc(self):
        try:
            self.cost_per_sqft = int(mk_int(self.curr_value) / mk_int(self.sqft))
        except ZeroDivisionError:
            self.cost_per_sqft = 0
        return self.cost_per_sqft

    @property
    def resign_calc(self):
        if int(self.resign_fee) > 80:
            self.resign_fee = int(self.resign_fee)
            return self.resign_fee
        else:
            return self.resign_fee

    @property
    def tenant_place_calc(self):
        if int(self.tenant_placement_fee) > 300:
            self.tenant_placement_fee = int(self.tenant_placement_fee)
            return self.tenant_placement_fee
        else:
            return self.tenant_placement_fee

    @property
    def maint_calc(self):
        if int(self.maintenance) > 300:
            self.maintenance = int(self.maintenance)
            return self.maintenance
        else:
            return self.maintenance

    @property
    def rtv_calc(self):
        getcontext().prec = 2
        try:
            self.rtv = float(Decimal(mk_int(self.rent)) / Decimal(mk_int(self.curr_value)))
        except ZeroDivisionError:
            self.rtv = 0.00
        self.rtv = self.rtv + 0
        return self.rtv

    @property
    def prop_mgmt_calc(self):
        self.prop_management_fee = int(.09 * self.rent)
        return self.prop_management_fee

    @property
    def closing_costs_calc(self):
        self.closing_costs = int(.03 * self.curr_value)
        return self.closing_costs
