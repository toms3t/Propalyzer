from django.test import TestCase
from ..context_data import ContextData
from ..secret import Secret
import requests

ZWSID = Secret.ZWSID


class PropertyModelTest(TestCase):
    def setUp(self):
        self.prop = ContextData()
        self.prop.create_test_obj()

    def test_property_attributes_should_be_persisted(self):
        self.assertEqual(
            self.prop.address,
            '3465-N-Main-St-Soquel-CA-95073'
        )
        self.assertEqual(
            self.prop.listing_url,
            'http://www.zillow.com/homedetails/3465-N-Main-St-Soquel-CA-95073/16128477_zpid/'
        )
        self.assertEqual(self.prop.neighborhood, 'Unknown')
        self.assertTrue(self.prop.pub_date)
        self.assertEqual(self.prop.curr_value, 699600)
        self.assertEqual(self.prop.value_low, 680101)
        self.assertEqual(self.prop.value_high, 751691)
        self.assertEqual(self.prop.initial_market_value, 699600)
        self.assertEqual(self.prop.initial_improvements, 5000)
        self.assertEqual(self.prop.rent, 2600)
        self.assertEqual(self.prop.rent_low, 2106)
        self.assertEqual(self.prop.rent_high, 2990)
        self.assertEqual(self.prop.sqft, 1058)
        self.assertEqual(self.prop.lot_sqft, 20343)
        self.assertEqual(self.prop.beds, 2)
        self.assertEqual(self.prop.baths, 1.5)
        self.assertEqual(self.prop.year_built, 1950)
        self.assertEqual(self.prop.hoa, 100)
        self.assertEqual(self.prop.maintenance, 800)
        self.assertEqual(self.prop.tenant_placement_fee, 500)
        self.assertEqual(self.prop.taxes, 2000)
        self.assertEqual(self.prop.utilities, 30)
        self.assertEqual(self.prop.insurance, 1000)
        self.assertEqual(self.prop.prop_management_fee, 234)
        self.assertEqual(self.prop.resign_fee, 300)
        self.assertEqual(self.prop.vacancy_rate, 0.08)
        self.assertEqual(self.prop.notes, '')
        self.assertEqual(self.prop.interest_rate, 4.75)
        self.assertEqual(self.prop.down_payment_percentage, 25.00)
        self.assertEqual(self.prop.schools, '')
        self.assertEqual(self.prop.school_scores, '')
        self.assertEqual(self.prop.county, 'Santa Cruz County')

    def test_property_should_return_address_when_converted_to_string(self):
        self.assertEqual(
            self.prop.__str__, '3465-N-Main-St-Soquel-CA-95073')

    def test_vacancy_calc_should_return_vacancy(self):
        self.assertEqual(self.prop.vacancy, 208)

    def test_oper_inc_calc_should_return_oper_income(self):
        self.assertEqual(self.prop.oper_income, 2392)

    def test_cost_per_sqft_calc_should_return_cost_per_sqft(self):
        self.assertEqual(self.prop.cost_per_sqft, 661)

    def test_down_payment_calc_should_return_down_payment(self):
        self.assertEqual(self.prop.down_payment, 174900)

    def test_total_mortgage_calc_should_return_total_mortgage(self):
        self.assertEqual(self.prop.total_mortgage, 524700)

    def test_init_cash_invested_calc_should_init_cash_invest(self):
        self.assertEqual(self.prop.init_cash_invest, 200888)

    def test_oper_exp_calc_should_return_oper_exp(self):
        self.assertEqual(self.prop.oper_exp, 655)

    def test_net_oper_income_calc_should_return_net_oper_income(self):
        self.assertEqual(self.prop.net_oper_income, 1737)

    def test_cash_flow_calc_should_return_cash_flow(self):
        self.assertEqual(self.prop.cash_flow, -1000)

    def test_oper_exp_ratio_calc_should_return_oper_exp_ratio(self):
        self.assertEqual(self.prop.oper_exp_ratio, .27)

    def test_debt_coverage_ratio_calc_should_return_none_if_no_mort_payment(self):
        if self.prop.mort_payment == 0:
            self.assertIsNone(self.prop.debt_cover_ratio)
        else:
            self.assertTrue(True)

    def test_debt_coverage_ratio_calc_should_return_debt_cover_ratio(self):
        self.assertEqual(self.prop.debt_cover_ratio, .63)

    def test_cap_rate_should_return_cap_rate(self):
        self.assertEqual(self.prop.cap_rate, 0.03)

    def test_cash_on_cash_should_return_cash_on_cash_return(self):
        self.assertEqual(self.prop.cash_on_cash_return, -0.0597)

    def test_mort_payment_calc_should_return_mort_payment(self):
        self.assertEqual(self.prop.mort_payment, 2737)

    def test_rtv_calc_should_return_rtv(self):
        self.assertEqual(self.prop.rtv, 0.0037)

    def test_prop_mgmt_calc_should_return_property_management_fee(self):
        self.assertEqual(self.prop.prop_management_fee, 234)

    def test_closing_costs_calc_should_return_closing_costs(self):
        self.assertEqual(self.prop.closing_costs, 20988)

    def test_zillow_api_key(self):
        resp = str(requests.get(
            f'http://www.zillow.com/webservice/GetZestimate.htm?zws-id={ZWSID}&zpid=48749425'))
        self.assertEqual(resp, '<Response [200]>')

    def test_net_oper_income(self):
        self.assertEqual(self.prop.oper_income -
                         self.prop.oper_exp, self.prop.net_oper_income)

    def test_cash_flow(self):
        self.assertEqual(self.prop.net_oper_income -
                         self.prop.mort_payment, self.prop.cash_flow)

    def test_fema_response(self):
        url1 = 'https://www.fema.gov/api/open/v1/DisasterDeclarationsSummaries?'
        url2 = '$filter=state eq TN&$select=state, incidentType, declaredCountyArea, title, '
        url3 = 'incidentEndDate&$orderby=incidentEndDate'
        url = url1+url2+url3
        resp = str(requests.get(url))
        self.assertEqual(resp, '<Response [200]>')
