
"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from .models import Property
from crispy_forms.layout import Layout, Submit, Field
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper


class AddressForm(forms.Form):
	text_input = forms.CharField()

	helper = FormHelper()
	helper.form_class = 'form-horizontal'
	helper.layout = Layout(
		Field('text_input', css_class='input-xlarge'),
		FormActions(
			Submit('save_changes', 'Save changes', css_class="btn-primary"),
			Submit('cancel', 'Cancel')
		)
	)

class PropertyForm(forms.ModelForm):
	class Meta:
		model = Property
		fields = [
			'address', 'curr_value', 'rent', 'sqft', 'down_payment_percentage',
			'interest_rate', 'closing_costs', 'initial_improvements', 'hoa', 'insurance',
			'taxes', 'utilities', 'maintenance', 'property_management_fee', 'tenant_placement_fee',
			'resign_fee', 'schools', 'county', 'year_built', 'owned', 'notes'
		]
		help_texts = {
			'sqft': 'Pulled from Zillow',
			'rent': 'Pulled from Zillow',
			'curr_value': 'Pulled from Zillow',
			'schools': 'Pulled from Zillow',
			'year_built': 'Pulled from Zillow',
			'county': 'Pulled from Zillow',
			'taxes': 'Defaults to $2000. If modifying this value, enter annual amount.',
			'insurance': 'Defaults to $1000. \
			If modifying this value, enter annual amount',
			'maintenance': 'Default value is an estimate for quick analysis purposes only. \
			If modifying this value, enter annual amount',
			'tenant_placement_fee': 'Enter annual amount',
			'resign_fee': 'Enter annual amount',
			'closing_costs': 'Estimated at 3% of zestimate',
			'hoa': 'This value is not auto-populated, please verify - Enter annual amount',
			'property_management_fee': 'Calculated at 9% of rent',
			'utilities': 'Enter *MONTHLY* amount'
		}


class AddressForm(forms.ModelForm):
	class Meta:
		model = Property
		fields = ['address']


class BootstrapAuthenticationForm(AuthenticationForm):
	"""Authentication form which uses boostrap CSS."""
	username = forms.CharField(max_length=254,
		widget=forms.TextInput({
			'class': 'form-control',
			'placeholder': 'User name'}))
	password = forms.CharField(label=_("Password"),
		widget=forms.PasswordInput({
			'class': 'form-control',
			'placeholder': 'Password'}))



