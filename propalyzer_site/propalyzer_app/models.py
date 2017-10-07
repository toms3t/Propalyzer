"""
Definition of models.
"""

from django.db import models
from django.utils import timezone
from decimal import Decimal, getcontext


class Property(models.Model):
    '''
    The Property class is used to create Property objects which contains all subject Property attributes
    '''
    user = models.CharField(max_length=200, blank=False)
    address = models.CharField(max_length=200, blank=False)
    listing_url = models.CharField(max_length=200, blank=False)
    neighborhood = models.CharField(max_length=200, blank=True, null=True)
    pub_date = models.DateTimeField(default=timezone.now)
    curr_value = models.IntegerField(default=0, blank=False)
    value_low = models.IntegerField(default=0, blank=False)
    value_high = models.IntegerField(default=0, blank=False)
    initial_market_value = models.IntegerField(default=0, blank=True)
    closing_costs = models.IntegerField(default=0, blank=False)
    initial_improvements = models.IntegerField(default=0, blank=False)
    rent = models.IntegerField(default=0, blank=False)
    rent_low = models.IntegerField(default=0, blank=False)
    rent_high = models.IntegerField(default=0, blank=False)
    sqft = models.IntegerField(default=0, blank=True)
    lot_sqft = models.IntegerField(default=0, blank=True)
    cost_per_sqft = models.IntegerField(default=0, blank=True)
    beds = models.IntegerField(default=0, blank=True)
    baths = models.FloatField(default=0.00, blank=True)
    year_built = models.IntegerField(default=0, blank=True)
    hoa = models.IntegerField(default=0, blank=False)
    leasing_fee = models.IntegerField(default=0, blank=False)
    maintenance = models.IntegerField(default=800, blank=False)
    tenant_placement_fee = models.IntegerField(default=0, blank=False)
    taxes = models.IntegerField(default=0, blank=False)
    utilities = models.IntegerField(default=0, blank=False)
    insurance = models.IntegerField(default=0, blank=False)
    property_management_fee = models.IntegerField(default=0, blank=False)
    resign_fee = models.IntegerField(default=0, blank=False)
    vacancy_rate = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, blank=True)
    vacancy = models.IntegerField(default=0, blank=True)
    income_inflation_rate = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, blank=True)
    exp_inflation_rate = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, blank=True)
    compounding_period = models.CharField(max_length=200, blank=True)
    selling_costs = models.IntegerField(default=0, blank=True)
    ltv_for_refinance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, blank=True)
    rtv = models.FloatField(default=0.00, blank=True)
    notes = models.TextField(null=True, blank=True)
    oper_income = models.IntegerField(default=0, blank=True)
    oper_exp = models.IntegerField(default=0, blank=True)
    net_oper_income = models.IntegerField(default=0, blank=True)
    cash_flow = models.IntegerField(default=0, blank=True)
    mort_payment = models.IntegerField(default=0, blank=True)
    interest_rate = models.FloatField(default=4.75, blank=True)
    total_mortgage = models.IntegerField(default=0, blank=True)
    down_payment_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=25, blank=False)
    down_payment = models.IntegerField(default=0, blank=False)
    init_cash_invest = models.IntegerField(default=0, blank=True)
    debt_cover_ratio = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, blank=True)
    cash_on_cash_return = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, blank=True)
    equity = models.IntegerField(default=0, blank=True)
    return_on_equity = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, blank=True)
    oper_exp_ratio = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, blank=True)
    cap_rate = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, blank=True)
    total_roi = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, blank=True)
    total_roi_w_tax_savings = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, blank=True)
    schools = models.CharField(max_length=200, blank=True)
    school_scores = models.CharField(max_length=200, blank=True)
    county = models.CharField(max_length=200, blank=True)
    crime_level = models.CharField(max_length=200, blank=True)
    nat_disasters = models.CharField(max_length=200, blank=True)
    owned = models.BooleanField(default=False)

    def __str__(self):
        return self.address

    def oper_inc_calc(self):
        self.oper_income = int(self.rent - self.vacancy)
        return self.oper_income

    def init_cash_invested_calc(self):
        self.init_cash_invest = int(self.down_payment + self.closing_costs + self.initial_improvements)
        return self.init_cash_invest

    def vacancy_calc(self):
        self.vacancy_rate = .08
        self.vacancy = int(self.vacancy_rate * self.rent)
        return self.vacancy

    def oper_exp_calc(self):
        self.oper_exp = int(((self.resign_fee / 12) + (self.taxes / 12) + (
        self.hoa / 12) + self.utilities + self.property_management_fee + (self.insurance / 12)
        + (self.maintenance / 12) + (self.tenant_placement_fee / 12)))
        return self.oper_exp

    def net_oper_income_calc(self):
        self.net_oper_income = int(self.oper_income - self.oper_exp)
        return self.net_oper_income

    def cash_flow_calc(self):
        self.cash_flow = int(self.net_oper_income - self.mort_payment)
        return self.cash_flow

    def oper_exp_ratio_calc(self):
        getcontext().prec = 2
        self.oper_exp_ratio = float(Decimal(self.oper_exp) / Decimal(self.oper_income))
        self.oper_exp_ratio = self.oper_exp_ratio + 0
        return self.oper_exp_ratio

    def debt_coverage_ratio_calc(self):
        getcontext().prec = 2
        if self.mort_payment:
            self.debt_cover_ratio = float(Decimal(self.net_oper_income) / Decimal(self.mort_payment))
            return self.debt_cover_ratio
        else:
            return None

    def cap_rate(self):
        getcontext().prec = 2
        self.initial_market_value = self.curr_value
        self.cap_rate = float(Decimal((self.net_oper_income * 12) / Decimal(self.initial_market_value)))
        self.cap_rate = self.cap_rate + 0
        return self.cap_rate

    def cash_on_cash(self):
        getcontext().prec = 3
        self.cash_on_cash_return = float(Decimal((self.cash_flow * 12) / Decimal(self.init_cash_invest)))
        self.cash_on_cash_return = self.cash_on_cash_return + 0
        return self.cash_on_cash_return

    def total_mortgage_calc(self):
        getcontext().prec = 8
        self.total_mortgage = self.curr_value - self.down_payment
        return self.total_mortgage

    def mort_payment_calc(self):
        i = (self.interest_rate / 100) / 12
        n = 360
        p = self.total_mortgage
        self.mort_payment = int(p * (i * (1 + i) ** n) / ((1 + i) ** n - 1))
        return self.mort_payment

    def cost_per_sqft_calc(self):
        self.cost_per_sqft = int(self.curr_value / self.sqft)
        return self.cost_per_sqft

    def taxes_calc(self):
        if self.taxes > 200:
            self.taxes = int(self.taxes)
            return self.taxes
        else:
            return self.taxes

    def insurance_calc(self):
        self.insurance = float(self.curr_value)*.0022
        return self.insurance

    def resign_calc(self):
        if self.resign_fee > 80:
            self.resign_fee = int(self.resign_fee)
            return self.resign_fee
        else:
            return self.resign_fee

    def tenant_place_calc(self):
        if self.tenant_placement_fee > 300:
            self.tenant_placement_fee = int(self.tenant_placement_fee)
            return self.tenant_placement_fee
        else:
            return self.tenant_placement_fee

    def maint_calc(self):
        if self.maintenance > 300:
            self.maintenance = int(self.maintenance)
            return self.maintenance
        else:
            return self.maintenance

    def rtv_calc(self):
        getcontext().prec = 2
        self.rtv = float(Decimal(self.rent) / Decimal(self.curr_value))
        self.rtv = self.rtv + 0
        return self.rtv

    def down_payment_calc(self):
        getcontext().prec = 8
        dpp = self.down_payment_percentage / 100.0
        self.down_payment = int((self.curr_value) * (dpp))
        return self.down_payment

    def prop_mgmt_calc(self):
        self.property_management_fee = int(.09 * self.rent)
        return self.property_management_fee

    def closing_costs_calc(self):
        self.closing_costs = int(.03 * self.curr_value)
        return self.closing_costs
