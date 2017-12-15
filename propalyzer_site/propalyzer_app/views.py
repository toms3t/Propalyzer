from datetime import datetime
import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.utils import timezone

from .forms import AddressForm
from .forms import PropertyForm
from .property import PropSetup

LOG = logging.getLogger(__name__)
PROP = object


@login_required
def address(request):
	"""
	Renders the starting page for entering a property address
	:param request: HTTP Request
	:return: app/address.html page
	"""

	if request.method == "POST":
		address_str = str(request.POST['text_input'])
		prop = PropSetup(address_str)
		prop.set_address()
		if prop.error:
			return TemplateResponse(request, 'app/addressnotfound.html')

		prop.set_zillow_url()
		if 'ConnectionError' in prop.error:
			return TemplateResponse(request, 'app/connection_error.html')
		if 'AddressNotFound' in prop.error:
			return TemplateResponse(request, 'app/addressnotfound.html')

		prop.set_xml_data()
		prop.set_areavibes_info()

		# Loggers
		LOG.debug('prop.address_str --- {}'.format(prop.address_str))
		LOG.debug('prop.address_dict --- {}'.format(prop.address_dict))
		LOG.debug('prop.url --- {}'.format(prop.url))
		LOG.debug('prop.zillow_dict --- {}'.format(prop.zillow_dict))
		LOG.debug('areavibes_dict--- {}'.format(prop.areavibes_dict))

		try:
			prop.prop_management_fee = int(.09 * int(prop.rent_zest))
		except ValueError:
			prop.prop_management_fee = 0
		prop.initial_market_value = prop.curr_value
		prop.initial_improvements = 0
		prop.insurance = 1000
		prop.maintenance = 800
		prop.taxes = 1500
		prop.hoa = 0
		prop.utilities = 0
		prop.interest_rate = 4.75
		prop.down_payment_percentage = 25
		prop.down_payment = int(prop.curr_value) * (prop.down_payment_percentage / 100.0)
		prop.closing_costs = int(.03 * int(prop.curr_value))

		global PROP
		PROP = prop
		return redirect('edit')
	else:
		context = {
			'title': 'Home Page',
			'year': datetime.now().year,
			'form': AddressForm(),
		}
		return TemplateResponse(request, 'app/address.html', context)


@login_required
def edit(request):
	"""
	Renders the 'app/edit.html' page for editing listing values
	:param request: HTTP Request
	:return: 'app/edit.html' page
	"""
	if request.method == "POST":
		form = PropertyForm(request.POST)
		PROP.sqft = int(form.data['sqft'])
		PROP.curr_value = int(form.data['curr_value'])
		PROP.rent_zest = int(form.data['rent'])
		PROP.down_payment_percentage = float(form.data['down_payment_percentage'])
		PROP.interest_rate = float(form.data['interest_rate'])
		PROP.closing_costs = int(form.data['closing_costs'])
		PROP.initial_improvements = int(form.data['initial_improvements'])
		PROP.hoa = int(form.data['hoa'])
		PROP.insurance = int(form.data['insurance'])
		PROP.taxes = int(form.data['taxes'])
		PROP.utilities = int(form.data['utilities'])
		PROP.maintenance = int(form.data['maintenance'])
		PROP.prop_management_fee = int(form.data['prop_management_fee'])
		PROP.tenant_placement_fee = int(form.data['tenant_placement_fee'])
		PROP.resign_fee = int(form.data['resign_fee'])
		PROP.schools = form.data['schools']
		PROP.county = form.data['county']
		PROP.year_built = int(form.data['year_built'])
		PROP.notes = form.data['notes']
		if form.is_valid():
			return redirect('results')
	else:
		form = PropertyForm(initial={
			'address': PROP.address_str,
			'curr_value': PROP.curr_value,
			'rent': PROP.rent_zest,
			'sqft': PROP.sqft,
			'down_payment_percentage': PROP.down_payment_percentage,
			'interest_rate': PROP.interest_rate,
			'closing_costs': PROP.closing_costs,
			'initial_improvements': PROP.initial_improvements,
			'hoa': PROP.hoa,
			'insurance': PROP.insurance,
			'taxes': PROP.taxes,
			'utilities': PROP.utilities,
			'maintenance': PROP.maintenance,
			'prop_management_fee': PROP.prop_management_fee,
			'tenant_placement_fee': PROP.tenant_placement_fee,
			'resign_fee': PROP.resign_fee,
			'schools': PROP.schools,
			'county': PROP.county,
			'year_built': PROP.year_built,
			'notes': PROP.notes
		}
		)
	return render(request, 'app/edit.html', {'form': form})


@login_required
def results(request):
	"""
	Renders the results page which displays listing information, operating income/expense, cash flow, and
	investment ratios.
	:param request: HTTP request
	:return: 'app/results.html' page
	"""
	context = {
		'address': PROP.address_str,
		'taxes': '$' + str(int(int(PROP.taxes) / 12)),
		'hoa': '$' + str(int(int(PROP.hoa) / 12)),
		'rent': '$' + str(PROP.rent_zest),
		'vacancy': '$' + str(PROP.vacancy_calc),
		'oper_income': '$' + str(PROP.oper_inc_calc),
		'total_mortgage': '$' + str(PROP.total_mortgage_calc),
		'down_payment_percentage': str(PROP.down_payment_percentage) + '%',
		'down_payment': '$' + str(PROP.down_payment_calc),
		'curr_value': '$' + str(PROP.curr_value),
		'init_cash_invest': '$' + str(PROP.init_cash_invested_calc),
		'oper_exp': '$' + str(PROP.oper_exp_calc),
		'net_oper_income': '$' + str(PROP.net_oper_income_calc),
		'cap_rate': '{0:.1f}%'.format(PROP.cap_rate_calc * 100),
		'initial_market_value': '$' + str(PROP.curr_value),
		'interest_rate': str(PROP.interest_rate) + '%',
		'mort_payment': '$' + str(PROP.mort_payment_calc),
		'sqft': PROP.sqft,
		'closing_costs': '$' + str(PROP.closing_costs),
		'initial_improvements': '$' + str(PROP.initial_improvements),
		'cost_per_sqft': '$' + str(PROP.cost_per_sqft_calc),
		'insurance': '$' + str(int(PROP.insurance / 12)),
		'maintenance': '$' + str(int(PROP.maint_calc / 12)),
		'prop_management_fee': '$' + str(PROP.prop_management_fee),
		'utilities': '$' + str(PROP.utilities),
		'tenant_placement_fee': '$' + str(int(PROP.tenant_place_calc / 12)),
		'resign_fee': '$' + str(int(PROP.resign_calc / 12)),
		'notes': PROP.notes,
		'pub_date': timezone.now,
		'rtv': '{0:.2f}%'.format(PROP.rtv_calc * 100),
		'cash_flow': '$' + str(PROP.cash_flow_calc),
		'oper_exp_ratio': '{0:.1f}'.format(PROP.oper_exp_ratio_calc * 100) + '%',
		'debt_coverage_ratio': PROP.debt_coverage_ratio_calc,
		'cash_on_cash': '{0:.2f}%'.format(PROP.cash_on_cash_calc * 100),
		'schools': 'Unknown',
		'school_scores': '0,0,0',
		'year_built': PROP.year_built,
		'county': PROP.county,
		'nat_disasters': 'Unknown',
		'listing_url': PROP.listing_url,
		'beds': PROP.beds,
		'baths': PROP.baths,
		'livability': PROP.areavibes_dict['livability'],
		'crime': PROP.areavibes_dict['crime'],
		'cost_of_living': PROP.areavibes_dict['cost_of_living'],
		'education': PROP.areavibes_dict['education'],
		'employment': PROP.areavibes_dict['employment'],
		'housing': PROP.areavibes_dict['housing'],
		'weather': PROP.areavibes_dict['weather']
	}
	return render(request, 'app/results.html', context)


def disclaimer(request):
	"""
	Renders the disclaimer page with specific paragraphs taken from Zillow.com terms of use
	:param request: HTTP Request
	:return: 'app/disclaimer.html' page
	"""
	return TemplateResponse(request, 'app/disclaimer.html')
