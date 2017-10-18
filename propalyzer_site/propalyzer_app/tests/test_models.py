from django.utils import timezone
from django.test import TestCase

from ..models import Property


class PropertyModelTest(TestCase):
    def setUp(self):
        self.property_object = Property.objects.create(
            user='zillow',
            address='3465-N-Main-St-Soquel-CA-95073',
            listing_url='http://www.zillow.com/homedetails/3465-N-Main-St-Soquel-CA-95073/16128477_zpid/',
            neighborhood='Unknown',
            pub_date=timezone.now(),
            curr_value=699600,
            value_low=680101,
            value_high=751691,
            initial_market_value=699600,
            initial_improvements=5000,
            rent=2600,
            rent_low=2106,
            rent_high=2990,
            sqft=1058,
            lot_sqft=20343,
            beds=2,
            baths=1.5,
            year_built=1950,
            hoa=100,
            maintenance=800,
            tenant_placement_fee=500,
            taxes=2000,
            utilities=30,
            insurance=1000,
            property_management_fee=234,
            resign_fee=300,
            vacancy_rate=0.08,
            rtv=0.00,
            notes='',
            interest_rate=4.75,
            down_payment_percentage=25.00,
            schools='',
            school_scores='',
            county='Santa Cruz County',
            crime_level='Unknown',
            nat_disasters='Unknown',
            owned=False
        )
        self.cost_per_sqft = self.property_object.cost_per_sqft_calc
        self.down_payment = self.property_object.down_payment_calc
        self.vacancy = self.property_object.vacancy_calc
        self.closing_costs = self.property_object.closing_costs_calc
        self.oper_income = self.property_object.oper_inc_calc
        self.oper_exp = self.property_object.oper_exp_calc
        self.net_oper_income = self.property_object.net_oper_income_calc
        self.total_mortgage = self.property_object.total_mortgage_calc
        self.mort_payment = self.property_object.mort_payment_calc
        self.cash_flow = self.property_object.cash_flow_calc
        self.oper_exp_ratio = self.property_object.oper_exp_ratio_calc
        self.debt_coverage_ratio = self.property_object.debt_coverage_ratio_calc

    def test_property_attributes_should_be_persisted(self):
        self.assertEqual(self.property_object.user, 'zillow')
        self.assertEqual(
            self.property_object.address,
            '3465-N-Main-St-Soquel-CA-95073'
        )
        self.assertEqual(
            self.property_object.listing_url,
            'http://www.zillow.com/homedetails/3465-N-Main-St-Soquel-CA-95073/16128477_zpid/'
        )
        self.assertEqual(self.property_object.neighborhood, 'Unknown')
        self.assertTrue(self.property_object.pub_date)
        self.assertEqual(self.property_object.curr_value, 699600)
        self.assertEqual(self.property_object.value_low, 680101)
        self.assertEqual(self.property_object.value_high, 751691)
        self.assertEqual(self.property_object.initial_market_value, 699600)
        self.assertEqual(self.property_object.initial_improvements, 5000)
        self.assertEqual(self.property_object.rent, 2600)
        self.assertEqual(self.property_object.rent_low, 2106)
        self.assertEqual(self.property_object.rent_high, 2990)
        self.assertEqual(self.property_object.sqft, 1058)
        self.assertEqual(self.property_object.lot_sqft, 20343)
        self.assertEqual(self.property_object.beds, 2)
        self.assertEqual(self.property_object.baths, 1.5)
        self.assertEqual(self.property_object.year_built, 1950)
        self.assertEqual(self.property_object.hoa, 100)
        self.assertEqual(self.property_object.maintenance, 800)
        self.assertEqual(self.property_object.tenant_placement_fee, 500)
        self.assertEqual(self.property_object.taxes, 2000)
        self.assertEqual(self.property_object.utilities, 30)
        self.assertEqual(self.property_object.insurance, 1000)
        self.assertEqual(self.property_object.property_management_fee, 234)
        self.assertEqual(self.property_object.resign_fee, 300)
        self.assertEqual(self.property_object.vacancy_rate, 0.08)
        self.assertEqual(self.property_object.notes, '')
        self.assertEqual(self.property_object.interest_rate, 4.75)
        self.assertEqual(self.property_object.down_payment_percentage, 25.00)
        self.assertEqual(self.property_object.schools, '')
        self.assertEqual(self.property_object.school_scores, '')
        self.assertEqual(self.property_object.county, 'Santa Cruz County')
        self.assertEqual(self.property_object.crime_level, 'Unknown')
        self.assertEqual(self.property_object.nat_disasters, 'Unknown')
        self.assertFalse(self.property_object.owned)

    def test_property_should_return_address_when_converted_to_string(self):
        self.assertEqual(
            self.property_object.__str__(), '3465-N-Main-St-Soquel-CA-95073')

    def test_vacancy_calc_should_return_vacancy(self):
        self.vacancy = self.property_object.vacancy_calc
        self.assertEqual(self.vacancy, 208)

    def test_oper_inc_calc_should_return_oper_income(self):
        self.oper_income = self.property_object.oper_inc_calc
        self.assertEqual(self.oper_income, 2392)

    def test_cost_per_sqft_calc_should_return_cost_per_sqft(self):
        self.cost_per_sqft = self.property_object.cost_per_sqft_calc
        self.assertEqual(self.cost_per_sqft, 661)

    def test_down_payment_calc_should_return_down_payment(self):
        self.down_payment = self.property_object.down_payment_calc
        self.assertEqual(self.down_payment, 174900)

    def test_total_mortgage_calc_should_return_total_mortgage(self):
        self.total_mortgage = self.property_object.total_mortgage_calc
        self.assertEqual(self.total_mortgage, 524700)

    def test_init_cash_invested_calc_should_init_cash_invest(self):
        self.init_cash_invest = self.property_object.init_cash_invested_calc
        self.assertEqual(self.init_cash_invest, 200888)

    def test_oper_exp_calc_should_return_oper_exp(self):
        self.oper_exp = self.property_object.oper_exp_calc
        self.assertEqual(self.oper_exp, 655)

    def test_net_oper_income_calc_should_return_net_oper_income(self):
        self.net_oper_income = self.property_object.net_oper_income_calc
        self.assertEqual(self.net_oper_income, 1737)

    def test_cash_flow_calc_should_return_cash_flow(self):
        self.cash_flow = self.property_object.cash_flow_calc
        self.assertEqual(self.cash_flow, -1000)

    def test_oper_exp_ratio_calc_should_return_oper_exp_ratio(self):
        self.oper_exp_ratio = self.property_object.oper_exp_ratio_calc
        self.assertEqual(self.oper_exp_ratio, .27)

    def test_debt_coverage_ratio_calc_should_return_none_if_no_mort_payment(self):
        if self.mort_payment == 0:
            self.debt_coverage_ratio = self.property_object.debt_coverage_ratio_calc
            self.assertIsNone(self.debt_coverage_ratio)
        else:
            self.assertTrue(True)

    def test_debt_coverage_ratio_calc_should_return_debt_cover_ratio(self):
        self.debt_coverage_ratio = self.property_object.debt_coverage_ratio_calc
        self.assertEqual(self.debt_coverage_ratio, .63)

    def test_cap_rate_should_return_cap_rate(self):
        self.cap_rate = self.property_object.cap_rate()
        self.assertEqual(self.cap_rate, 0.03)

    def test_cash_on_cash_should_return_cash_on_cash_return(self):
        cash_on_cash = self.property_object.cash_on_cash()
        self.assertEqual(cash_on_cash, 0.0)

    def test_mort_payment_calc_should_return_mort_payment(self):
        self.mort_payment = self.property_object.mort_payment_calc
        self.assertEqual(self.mort_payment, 2737)

    def test_rtv_calc_should_return_rtv(self):
        self.rtv = self.property_object.rtv_calc
        self.assertEqual(self.rtv, 0.0037)

    def test_prop_mgmt_calc_should_return_property_management_fee(self):
        self.property_management_fee = self.property_object.prop_mgmt_calc
        self.assertEqual(self.property_management_fee, 234)

    def test_closing_costs_calc_should_return_closing_costs(self):
        self.closing_costs = self.property_object.closing_costs_calc
        self.assertEqual(self.closing_costs, 20988)
