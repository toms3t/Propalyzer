from django.utils import timezone
from decimal import Decimal, getcontext


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


class ContextData:
    """
    Class to create property objects and execute the Zillow API call business logic.
    """

    def __init__(self):
        self.address = ''
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

    def set_data(self, data):
        for key in data.keys():
            self.__dict__[key] = data[key]
        return {
            'address': self.address,
            'taxes': '$' + str(int(int(self.taxes) / 12)),
            'hoa': '$' + str(int(int(self.hoa) / 12)),
            'rent': '$' + str(self.rent),
            'vacancy': '$' + str(self.vacancy_calc),
            'oper_income': '$' + str(self.oper_inc_calc),
            'total_mortgage': '$' + str(self.total_mortgage_calc),
            'down_payment_percentage': str(self.down_payment_percentage) + '%',
            'down_payment': '$' + str(self.down_payment_calc),
            'curr_value': '$' + str(self.curr_value),
            'init_cash_invest': '$' + str(self.init_cash_invested_calc),
            'oper_exp': '$' + str(self.oper_exp_calc),
            'net_oper_income': '$' + str(self.net_oper_income_calc),
            'cap_rate': '{0:.1f}%'.format(self.cap_rate_calc * 100),
            'initial_market_value': '$' + str(self.curr_value),
            'interest_rate': str(self.interest_rate) + '%',
            'mort_payment': '$' + str(self.mort_payment_calc),
            'sqft': self.sqft,
            'closing_costs': '$' + str(self.closing_costs),
            'initial_improvements': '$' + str(self.initial_improvements),
            'cost_per_sqft': '$' + str(self.cost_per_sqft_calc),
            'insurance': '$' + str(int(int(self.insurance) / 12)),
            'maintenance': '$' + str(int(int(self.maint_calc) / 12)),
            'prop_management_fee': '$' + str(self.prop_management_fee),
            'utilities': '$' + str(self.utilities),
            'tenant_placement_fee': '$' + str(int(int(self.tenant_place_calc) / 12)),
            'resign_fee': '$' + str(int(int(self.resign_calc) / 12)),
            'notes': self.notes,
            'pub_date': timezone.now,
            'rtv': '{0:.2f}%'.format(self.rtv_calc * 100),
            'cash_flow': '$' + str(self.cash_flow_calc),
            'oper_exp_ratio': '{0:.1f}'.format(self.oper_exp_ratio_calc * 100) + '%',
            'debt_coverage_ratio': self.debt_coverage_ratio_calc,
            'cash_on_cash': '{0:.2f}%'.format(self.cash_on_cash_calc * 100),
            'elem_school': self.schools['elem_school'],
            'elem_school_score': self.schools['elem_school_score'],
            'mid_school': self.schools['mid_school'],
            'mid_school_score': self.schools['mid_school_score'],
            'high_school': self.schools['high_school'],
            'high_school_score': self.schools['high_school_score'],
            'year_built': self.year_built,
            'county': self.county,
            'nat_disasters': 'Unknown',
            'listing_url': self.listing_url,
            'beds': self.beds,
            'baths': self.baths,
            'livability': self.areavibes_dict['livability'],
            'crime': self.areavibes_dict['crime'],
            'cost_of_living': self.areavibes_dict['cost_of_living'],
            'schools': self.areavibes_dict['schools'],
            'employment': self.areavibes_dict['employment'],
            'housing': self.areavibes_dict['housing'],
            'weather': self.areavibes_dict['weather'],
            'disaster1_type': self.disaster_dict['1'][0],
            'disaster1_date': self.disaster_dict['1'][1],
            'disaster1_county': self.disaster_dict['1'][2],
            'disaster1_url': self.disaster_dict['1'][4],
            'disaster1_title': self.disaster_dict['1'][5],
            'disaster2_type': self.disaster_dict['2'][0],
            'disaster2_date': self.disaster_dict['2'][1],
            'disaster2_county': self.disaster_dict['2'][2],
            'disaster2_url': self.disaster_dict['2'][4],
            'disaster2_title': self.disaster_dict['2'][5],
            'disaster3_type': self.disaster_dict['3'][0],
            'disaster3_date': self.disaster_dict['3'][1],
            'disaster3_county': self.disaster_dict['3'][2],
            'disaster3_url': self.disaster_dict['3'][4],
            'disaster3_title': self.disaster_dict['3'][5],
            'disaster4_type': self.disaster_dict['4'][0],
            'disaster4_date': self.disaster_dict['4'][1],
            'disaster4_county': self.disaster_dict['4'][2],
            'disaster4_url': self.disaster_dict['4'][4],
            'disaster4_title': self.disaster_dict['4'][5],
            'disaster5_type': self.disaster_dict['5'][0],
            'disaster5_date': self.disaster_dict['5'][1],
            'disaster5_county': self.disaster_dict['5'][2],
            'disaster5_url': self.disaster_dict['5'][4],
            'disaster5_title': self.disaster_dict['5'][5],
        }

    @property
    def oper_inc_calc(self):
        self.oper_income = int(mk_int(self.rent) - self.vacancy)
        return self.oper_income

    @property
    def init_cash_invested_calc(self):
        self.down_payment = self.down_payment_calc
        self.init_cash_invest = int(
            self.down_payment + mk_int(self.closing_costs) + mk_int(self.initial_improvements))
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
            self.oper_exp_ratio = float(
                Decimal(self.oper_exp) / Decimal(self.oper_income))
        except ZeroDivisionError:
            self.oper_exp_ratio = 0.00
        self.oper_exp_ratio = self.oper_exp_ratio + 0
        return self.oper_exp_ratio

    @property
    def debt_coverage_ratio_calc(self):
        getcontext().prec = 2
        if self.mort_payment:
            try:
                self.debt_cover_ratio = float(
                    Decimal(self.net_oper_income) / Decimal(self.mort_payment))
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
            self.cap_rate = float(
                Decimal((self.net_oper_income * 12) / Decimal(self.initial_market_value)))
        except ZeroDivisionError:
            self.cap_rate = 0.00
        self.cap_rate = self.cap_rate + 0
        return self.cap_rate

    @property
    def cash_on_cash_calc(self):
        getcontext().prec = 3
        try:
            self.cash_on_cash_return = float(
                Decimal((self.cash_flow * 12) / Decimal(self.init_cash_invest)))
        except ZeroDivisionError:
            self.cash_on_cash_return = 0.00
        return self.cash_on_cash_return

    @property
    def down_payment_calc(self):
        self.down_payment = int(
            (float(self.down_payment_percentage) * mk_int(self.curr_value)) / 100)
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
            self.cost_per_sqft = int(
                mk_int(self.curr_value) / mk_int(self.sqft))
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
            self.rtv = float(Decimal(mk_int(self.rent)) /
                             Decimal(mk_int(self.curr_value)))
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

    @property
    def __str__(self):
        return self.address
