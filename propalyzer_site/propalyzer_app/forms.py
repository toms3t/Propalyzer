
"""
Definition of forms.
"""

from django import forms
from crispy_forms.layout import Layout, Submit, Field
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper


class AddressForm(forms.Form):
    text_input = forms.CharField(label='Residential Address')
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        Field('text_input', css_class='input-xlarge'),
        FormActions(
            Submit('save_changes', 'Save changes', css_class="btn-primary"),
            Submit('cancel', 'Cancel')
        )
    )


class PropertyForm(forms.Form):
    address = forms.CharField(label='Address', max_length=150)
    sqft = forms.IntegerField(label='SQFT', help_text='Pulled from Zillow.com')
    rent = forms.IntegerField(label='Rent', help_text='Pulled from Zillow.com')
    curr_value = forms.IntegerField(
        label='Zestimate (Current Value)', help_text='Pulled from Zillow.com')
    down_payment_percentage = forms.FloatField(
        label='Down Payment %', max_value=100)
    interest_rate = forms.FloatField(
        label='Mortgage Interest Rate %', max_value=99)
    closing_costs = forms.IntegerField(
        label='Closing Costs', help_text='Estimated at 3% of Zestimate')
    initial_improvements = forms.IntegerField(
        label='Initial Improvement Costs',
        help_text='Enter any costs to renovate property', required=False)
    hoa = forms.IntegerField(
        label='HOA', help_text='Enter annual amount', required=False)
    insurance = forms.CharField(
        label='Insurance', max_length=150, help_text='Defaults at $1000 If modifying, enter annual amount')
    taxes = forms.IntegerField(
        label='Taxes', help_text='Defaults to $1500. If modifying, enter annual amount')
    utilities = forms.IntegerField(
        label='Utility Costs',
        help_text='If you will pay utility costs instead of the tenant -- enter monthly amount', required=False)
    maintenance = forms.IntegerField(
        label='Maintenance Costs',
        help_text='Defaults to $800. If modifying, enter annual amount')
    prop_management_fee = forms.IntegerField(
        label='Prop Management Fee', help_text='Enter $ amount. Defaults to 9% of rent amount')
    tenant_placement_fee = forms.IntegerField(
        label='Tenant Placement Fee', help_text='Enter annual amount', required=False)
    resign_fee = forms.IntegerField(
        label='Resign Fee', help_text='Enter annual amount', required=False)
    county = forms.CharField(label='County', max_length=150,
                             required=False, help_text='Pulled from Zillow.com')
    year_built = forms.IntegerField(
        label='Year Built', help_text='Pulled from Zillow.com')
    notes = forms.CharField(
        label='Your Notes', widget=forms.Textarea, required=False)
