from django.utils import timezone
from django.test import TestCase

from ..models import Property


class PropertyModelTest(TestCase):
    def setUp(self):
        self.property_object = Property.objects.create(
            user='zillow',
            address='3465-N-Main-St-Soquel-CA-95073',
            listing_url='http://www.zillow.com/',
            neighborhood='Unknown',
            pub_date=timezone.now(),
            curr_value=699600,
            value_low=601655,
            value_high=755567,
            initial_market_value=699599,
            closing_costs=20987,
            initial_improvements=0,
            rent=2695,
            rent_low=2102,
            rent_high=3180,
            sqft=1058,
            lot_sqft=20343,
            cost_per_sqft=0,
            beds=2,
            baths=1.5,
            year_built=1950,
            hoa=0,
            leasing_fee=0,
            maintenance=800,
            tenant_placement_fee=0,
            taxes=0,
            utilities=0,
            insurance=1539,
            property_management_fee=242,
            resign_fee=0,
            vacancy=0.00,
            income_inflation_rate=0.00,
            exp_inflation_rate=0.00,
            compounding_period='',
            selling_costs=0,
            ltv_for_refinance=0.00,
            rtv=0.0,
            notes='',
            oper_income=200,
            oper_exp=0,
            net_oper_income=0,
            cash_flow=0,
            mort_payment=0,
            interest_rate=4.75,
            total_mortgage=0,
            down_payment_percentage=25.00,
            down_payment=174899,
            init_cash_invest=500,
            debt_cover_ratio=0.00,
            cash_on_cash_return=0.00,
            equity=0,
            return_on_equity=0,
            oper_exp_ratio=0.00,
            total_roi=0.00,
            total_roi_w_tax_savings=0.00,
            schools='',
            school_scores='',
            county='Santa Cruz County',
            crime_level='Unknown',
            nat_disasters='Unknown',
            owned=False
        )

    def test_property_attributes_should_be_persisted(self):
        self.assertEqual(self.property_object.user, 'zillow')
        self.assertEqual(
            self.property_object.address,
            '3465-N-Main-St-Soquel-CA-95073'
        )
        self.assertEqual(
            self.property_object.listing_url,
            'http://www.zillow.com/'
        )
        self.assertEqual(self.property_object.neighborhood, 'Unknown')
        self.assertTrue(self.property_object.pub_date)
        self.assertEqual(self.property_object.curr_value, 699600)
        self.assertEqual(self.property_object.value_low, 601655)
        self.assertEqual(self.property_object.value_high, 755567)
        self.assertEqual(self.property_object.initial_market_value, 699599)
        self.assertEqual(self.property_object.closing_costs, 20987)
        self.assertEqual(self.property_object.initial_improvements, 0)
        self.assertEqual(self.property_object.rent, 2695)
        self.assertEqual(self.property_object.rent_low, 2102)
        self.assertEqual(self.property_object.rent_high, 3180)
        self.assertEqual(self.property_object.sqft, 1058)
        self.assertEqual(self.property_object.lot_sqft, 20343)
        self.assertEqual(self.property_object.cost_per_sqft, 0)
        self.assertEqual(self.property_object.beds, 2)
        self.assertEqual(self.property_object.baths, 1.5)
        self.assertEqual(self.property_object.year_built, 1950)
        self.assertEqual(self.property_object.hoa, 0)
        self.assertEqual(self.property_object.leasing_fee, 0)
        self.assertEqual(self.property_object.maintenance, 800)
        self.assertEqual(self.property_object.tenant_placement_fee, 0)
        self.assertEqual(self.property_object.taxes, 0)
        self.assertEqual(self.property_object.utilities, 0)
        self.assertEqual(self.property_object.insurance, 1539)
        self.assertEqual(self.property_object.property_management_fee, 242)
        self.assertEqual(self.property_object.resign_fee, 0)
        self.assertEqual(self.property_object.vacancy, 0.00)
        self.assertEqual(self.property_object.income_inflation_rate, 0.00)
        self.assertEqual(self.property_object.exp_inflation_rate, 0.00)
        self.assertEqual(self.property_object.compounding_period, '')
        self.assertEqual(self.property_object.selling_costs, 0)
        self.assertEqual(self.property_object.ltv_for_refinance, 0.00)
        self.assertEqual(self.property_object.rtv, 0.0)
        self.assertEqual(self.property_object.notes, '')
        self.assertEqual(self.property_object.oper_income, 200)
        self.assertEqual(self.property_object.oper_exp, 0)
        self.assertEqual(self.property_object.net_oper_income, 0)
        self.assertEqual(self.property_object.cash_flow, 0)
        self.assertEqual(self.property_object.mort_payment, 0)
        self.assertEqual(self.property_object.interest_rate, 4.75)
        self.assertEqual(self.property_object.total_mortgage, 0)
        self.assertEqual(self.property_object.down_payment_percentage, 25.00)
        self.assertEqual(self.property_object.down_payment, 174899)
        self.assertEqual(self.property_object.init_cash_invest, 500)
        self.assertEqual(self.property_object.debt_cover_ratio, 0.00)
        self.assertEqual(self.property_object.cash_on_cash_return, 0.00)
        self.assertEqual(self.property_object.equity, 0)
        self.assertEqual(self.property_object.return_on_equity, 0)
        self.assertEqual(self.property_object.oper_exp_ratio, 0.00)
        self.assertEqual(self.property_object.total_roi, 0.00)
        self.assertEqual(self.property_object.total_roi_w_tax_savings, 0.00)
        self.assertEqual(self.property_object.schools, '')
        self.assertEqual(self.property_object.school_scores, '')
        self.assertEqual(self.property_object.county, 'Santa Cruz County')
        self.assertEqual(self.property_object.crime_level, 'Unknown')
        self.assertEqual(self.property_object.nat_disasters, 'Unknown')
        self.assertFalse(self.property_object.owned)

    def test_property_should_return_address_when_converted_to_string(self):
        self.assertEqual(
            self.property_object.__str__(),
            '3465-N-Main-St-Soquel-CA-95073'
        )

    def test_oper_inc_calc_should_return_oper_income(self):
        oper_income = self.property_object.oper_inc_calc()
        self.assertEqual(oper_income, 2695)

    def test_init_cash_invested_calc_should_init_cash_invest(self):
        init_cash_invest = self.property_object.init_cash_invested_calc()
        self.assertEqual(init_cash_invest, 195886)

    def test_vacancy_calc_should_return_vacancy(self):
        vacancy = self.property_object.vacancy_calc()
        self.assertEqual(vacancy, 215)

    def test_oper_exp_calc_should_return_oper_exp(self):
        oper_exp = self.property_object.oper_exp_calc()
        self.assertEqual(oper_exp, 436)

    def test_net_oper_income_calc_should_return_net_oper_income(self):
        net_oper_income = self.property_object.net_oper_income_calc()
        self.assertEqual(net_oper_income, 200)

    def test_cash_flow_calc_should_return_cash_flow(self):
        cash_flow = self.property_object.cash_flow_calc()
        self.assertEqual(cash_flow, 0)

    def test_oper_exp_ratio_calc_should_return_oper_exp_ratio(self):
        oper_exp_ratio = self.property_object.oper_exp_ratio_calc()
        self.assertEqual(oper_exp_ratio, 0.0)

    def test_debt_coverage_ratio_calc_should_return_none_if_no_mort_payment(
        self
    ):
        debt_coverage_ratio = self.property_object.debt_coverage_ratio_calc()
        self.assertIsNone(debt_coverage_ratio)

    def test_debt_coverage_ratio_calc_should_return_debt_cover_ratio(
        self
    ):
        self.property_object.mort_payment = 100
        self.property_object.save()

        debt_coverage_ratio = self.property_object.debt_coverage_ratio_calc()
        self.assertEqual(debt_coverage_ratio, 0.0)

    def test_cap_rate_should_return_cap_rate(self):
        cap_rate = self.property_object.cap_rate()
        self.assertEqual(cap_rate, 0.0)

    def test_cash_on_cash_should_return_cash_on_cash_return(self):
        cash_on_cash = self.property_object.cash_on_cash()
        self.assertEqual(cash_on_cash, 0.0)

    def test_total_mortgage_calc_should_return_total_mortgage(self):
        total_mortgage = self.property_object.total_mortgage_calc()
        self.assertEqual(total_mortgage, 524701)

    def test_mort_payment_calc_should_return_mort_payment(self):
        mort_payment = self.property_object.mort_payment_calc()
        self.assertEqual(mort_payment, 0)

    def test_cost_per_sqft_calc_should_return_cost_per_sqft(self):
        cost_per_sqft = self.property_object.cost_per_sqft_calc()
        self.assertEqual(cost_per_sqft, 661)

    def test_taxes_calc_should_return_int_value_if_greater_than_200(self):
        self.property_object.taxes = 201.99
        self.property_object.save()

        taxes = self.property_object.taxes_calc()
        self.assertEqual(taxes, 201)

    def test_taxes_calc_should_return_tax_if_not_greater_than_200(self):
        self.property_object.taxes = 199.99
        self.property_object.save()

        taxes = self.property_object.taxes_calc()
        self.assertEqual(taxes, 199.99)

    def test_insurance_calc_should_return_insurance(self):
        insurance = self.property_object.insurance_calc()
        self.assertEqual(insurance, 1539.1200000000001)

    def test_resign_calc_should_return_int_value_if_greater_than_80(self):
        self.property_object.resign_fee = 81.91
        self.property_object.save()

        resign = self.property_object.resign_calc()
        self.assertEqual(resign, 81)

    def test_resign_calc_should_return_resign_fee_if_not_greater_than_80(self):
        self.property_object.resign_fee = 79.91
        self.property_object.save()

        resign = self.property_object.resign_calc()
        self.assertEqual(resign, 79.91)

    def test_tenant_place_calc_should_return_int_value_if_greater_than_300(
        self
    ):
        self.property_object.tenant_placement_fee = 301.55
        self.property_object.save()

        tenant_placement_fee = self.property_object.tenant_place_calc()
        self.assertEqual(tenant_placement_fee, 301)

    def test_tenant_place_calc_should_return_fee_if_not_greater_than_300(self):
        self.property_object.tenant_placement_fee = 298.11
        self.property_object.save()

        tenant_placement_fee = self.property_object.tenant_place_calc()
        self.assertEqual(tenant_placement_fee, 298.11)

    def test_maint_calc_should_return_int_value_if_greater_than_300(self):
        self.property_object.maintenance = 301.55
        self.property_object.save()

        maintenance = self.property_object.maint_calc()
        self.assertEqual(maintenance, 301)

    def test_maint_calc_should_return_fee_if_not_greater_than_300(self):
        self.property_object.maintenance = 298.11
        self.property_object.save()

        maintenance = self.property_object.maint_calc()
        self.assertEqual(maintenance, 298.11)

    def test_rtv_calc_should_return_rtv(self):
        rtv = self.property_object.rtv_calc()
        self.assertEqual(rtv, 0.0039)

    def test_down_payment_calc_should_return_down_payment(self):
        down_payment = self.property_object.down_payment_calc()
        self.assertEqual(down_payment, 174900)

    def test_prop_mgmt_calc_shuold_return_property_management_fee(self):
        property_management_fee = self.property_object.prop_mgmt_calc()
        self.assertEqual(property_management_fee, 242)

    def test_closing_costs_calc_should_return_closing_costs(self):
        closing_costs = self.property_object.closing_costs_calc()
        self.assertEqual(closing_costs, 20988)
