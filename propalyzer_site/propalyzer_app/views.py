from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse
from django.template import loader
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import Property
from .forms import PropertyForm
from .forms import AddressForm
from .county import County
import re
import usaddress
from collections import defaultdict
from decimal import Decimal
import requests

# GLOBALS
ZWSID = ''
DETAILS_XML = ''


@login_required
def address(request):
	'''
	Renders the starting page for entering a property address
	:param request: HTTP Request
	:return: app/address.html page
	'''
	cash_flow_sum = 0
	researched_properties = Property.objects.filter(user=request.user)
	researched_property_list = researched_properties.order_by('-pub_date')
	owned_properties = Property.objects.filter(owned=True, user=request.user)
	owned_property_list = owned_properties.order_by('-pub_date')
	for prop in owned_properties:
		cash_flow_sum = cash_flow_sum + prop.cash_flow
	form = AddressForm()
	if request.method == "POST":
		address_str = str(request.POST['address'])
		address_parsed = usaddress.parse(address_str)
		addressdict = defaultdict(str)
		for item in address_parsed:
			addressdict[item[1]] = item[0]
		api_url1 = 'http://www.zillow.com/webservice/GetDeepSearchResults.htm?'
		api_url2 = 'zws-id={ZWSID}&address={num}+{dir}+{street}+{st_type}&citystatezip={city}%2C+{state}+{zip}&' \
					'rentzestimate=true'.format(ZWSID=ZWSID, num=addressdict['AddressNumber'],
					dir=addressdict['StreetNamePreDirectional'],
					street=addressdict['StreetName'], st_type=addressdict['StreetNamePostType'],
					city=addressdict['PlaceName'], state=addressdict['StateName'], zip=addressdict['ZipCode'])
		api_url = api_url1+api_url2
		prop_data = requests.get(api_url)
		global DETAILS_XML
		DETAILS_XML = str(prop_data.content)
		if 'no exact match' in DETAILS_XML:
			return TemplateResponse(request, 'app/addressnotfound.html')
		address, listing_url, county_code, sqft, lot_sqft, baths, beds, curr_value, value_low, value_high = get_listing_details(DETAILS_XML)[:10]
		rent_zest, rent_low, rent_high, year_built, last_sold_date, neighborhood = get_listing_details(DETAILS_XML)[10:]
		county = County.county_finder(county_code)
		new_prop = Property(
			address=address, sqft=sqft, rent=rent_zest, rent_low = rent_low, rent_high = rent_high, curr_value=curr_value,
			value_low = value_low, value_high = value_high, year_built=year_built, interest_rate=4.75, county=county,
			crime_level='Unknown', nat_disasters='Unknown', lot_sqft=lot_sqft, neighborhood=neighborhood, listing_url=listing_url,
			beds=beds, baths=baths
		)
		new_prop.property_management_fee = int(.09 * int(new_prop.rent))
		new_prop.initial_market_value = new_prop.curr_value
		new_prop.insurance = float(curr_value)*.0022
		new_prop.down_payment = int(new_prop.curr_value) * \
			(new_prop.down_payment_percentage / Decimal(100))
		new_prop.closing_costs = int(.03 * int(new_prop.curr_value))
		new_prop.user = request.user
		new_prop.save()
		pk = new_prop.pk
		post = get_object_or_404(Property, pk=pk)
		form = PropertyForm(instance=post)
		return redirect('edit', pk=post.pk)
	else:
		context = {
			'title': 'Home Page',
			'year': datetime.now().year,
			'researched_property_list': researched_property_list,
			'owned_property_list': owned_property_list,
			'form': AddressForm(),
			'cash_flow_sum': cash_flow_sum,
		}
		return TemplateResponse(request, 'app/address.html', context)


def get_listing_details(DETAILS_XML):
	"""
	Method to parse listing details from the XML received from API Call
	:param DETAILS_XML: XML document from Zillow API Call
	:return: list of property details
	"""
	address = re.findall('zillow.com/homedetails/(.*?)/', DETAILS_XML)[0]
	listing_url = re.findall('<homedetails>(.*?)</homedetails>', DETAILS_XML)[0]
	county_code = re.findall('<FIPScounty>(\d+)</FIPScounty>', DETAILS_XML)[0]
	sqft = re.findall('<finishedSqFt>(\d+)</finishedSqFt>',DETAILS_XML)[0]
	lot_sqft = re.findall('<lotSizeSqFt>(\d+)</lotSizeSqFt>',DETAILS_XML)[0]
	baths = re.findall('<bathrooms>(.*?)</bathrooms>', DETAILS_XML)[0]
	beds = re.findall('<bedrooms>(\d+)</bedrooms>', DETAILS_XML)[0]
	curr_value = re.findall('<zestimate><amount currency="USD">(\d+)</amount>', DETAILS_XML)[0]
	value_low, value_high = re.findall('>(\d+)</low><high currency="USD">(\d+)</high>.*?</zestimate>', DETAILS_XML)[0]
	rent_zest = re.findall('<rentzestimate><amount currency="USD">(\d+)</amount>', DETAILS_XML)[0]
	rent_low, rent_high = re.findall('<rentzestimate>.*?(\d+)</low><high currency="USD">(\d+)</high>.*?</rentzestimate>', DETAILS_XML)[0]
	year_built = re.findall('<yearBuilt>(\d+)</yearBuilt>', DETAILS_XML)[0]
	try:
		last_sold_date = re.findall('<lastSoldDate>(.*?)</lastSoldDate>', DETAILS_XML)[0]
	except:
		last_sold_date = 'Unknown'
	try:
		neighborhood = re.findall('<localRealEstate><region name="(.*?)" .*? type="neighborhood">', DETAILS_XML)[0]
	except:
		neighborhood = 'Unknown'
	listing_details = [
		address,
		listing_url,
		county_code,
		sqft,
		lot_sqft,
		baths,
		beds,
		curr_value,
		value_low,
		value_high,
		rent_zest,
		rent_low,
		rent_high,
		year_built,
		last_sold_date,
		neighborhood
	]
	return listing_details


@login_required
def edit(request, pk):
	'''
	Renders the 'app/edit.html' page for editing listing values
	:param request: HTTP Request
	:param pk: Primary Key - identifies the specific database record that corresponds with the listing details
	:return: 'app/edit.html' page
	'''
	post = get_object_or_404(Property, pk=pk)
	if request.method == "POST":
		form = PropertyForm(request.POST, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.published_date = timezone.now()
			post.save()
			return redirect('results', pk=post.pk)
	else:
		form = PropertyForm(instance=post)
	return render(request, 'app/edit.html', {'form': form})


@login_required
def results(request, pk):
	'''
	This view renders the results page which displays listing information, operating income/expense, cash flow, and
	investment ratios.
	:param request: HTTP request
	:param pk: Primary Key - identifies the specific database record that corresponds with the listing details
	:return: 'app/results.html' page
	'''
	prop = Property.objects.get(pk=pk)
	context = {
		'id': prop,
		'pkey': prop.pk,
		'address': prop.address.replace("-", " "),
		'taxes': '$'+str(int(prop.taxes_calc()/12)),
		'hoa': '$'+str(int(prop.hoa/12)),
		'rent': '$'+str(prop.rent),
		'vacancy': '$'+str(prop.vacancy_calc()),
		'oper_income': '$'+str(prop.oper_inc_calc()),
		'total_mortgage': '$'+str(prop.total_mortgage_calc()),
		'down_payment_percentage': str(prop.down_payment_percentage)+'%',
		'down_payment': '$'+str(prop.down_payment_calc()),
		'curr_value': '$'+str(prop.curr_value),
		'init_cash_invest': '$'+str(prop.init_cash_invested_calc()),
		'oper_exp': '$'+str(prop.oper_exp_calc()),
		'net_oper_income': '$'+str(prop.net_oper_income_calc()),
		'cash_flow': '$'+str(prop.cash_flow_calc()),
		'oper_exp_ratio': '{0:.1f}'.format(prop.oper_exp_ratio_calc()*100),
		'debt_coverage_ratio': prop.debt_coverage_ratio_calc(),
		'cap_rate': '{0:.1f}%'.format(prop.cap_rate()*100),
		'initial_market_value': '$'+str(prop.curr_value),
		'cash_on_cash': '{0:.2f}%'.format(prop.cash_on_cash()*100),
		'interest_rate': str(prop.interest_rate)+'%',
		'mort_payment': '$'+str(prop.mort_payment_calc()),
		'sqft': prop.sqft,
		'closing_costs': '$'+str(prop.closing_costs),
		'initial_improvements': '$'+str(prop.initial_improvements),
		'cost_per_sqft': '$'+str(prop.cost_per_sqft_calc()),
		'insurance': '$'+str(int(prop.insurance_calc()/12)),
		'maintenance': '$'+str(int(prop.maint_calc()/12)),
		'property_management_fee': '$'+str(prop.property_management_fee),
		'utilities': '$'+str(prop.utilities),
		'tenant_placement_fee': '$'+str(int(prop.tenant_place_calc()/12)),
		'resign_fee': '$'+str(int(prop.resign_calc()/12)),
		'notes': prop.notes,
		'pub_date': prop.pub_date,
		'rtv': '{0:.2f}%'.format(prop.rtv_calc()*100),
		'schools': 'test',
		'school_scores': '9,5,5',
		'year_built': prop.year_built,
		'county': prop.county,
		'crime_level': prop.crime_level,
		'nat_disasters': prop.nat_disasters,
		'listing_url': prop.listing_url,
		'beds': prop.beds,
		'baths': prop.baths
		}

	template = loader.get_template('app/results.html')
	return HttpResponse(template.render(context))


def disclaimer(request):
	'''
	Specific paragraphs taken from Zillow.com terms of use
	:param request: HTTP Request
	:return: 'app/disclaimer.html' page
	'''
	return TemplateResponse(request, 'app/disclaimer.html')
