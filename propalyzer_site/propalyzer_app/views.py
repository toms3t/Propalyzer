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
			crime_level='pass', nat_disasters='pass', lot_sqft=lot_sqft, neighborhood=neighborhood, listing_url=listing_url,
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
def results(request,pk):
	'''
	This view renders the results page which displays listing information, operating income/expense, cash flow, and
	investment ratios.
	:param request: HTTP request
	:param pk: Primary Key - identifies the specific database record that corresponds with the listing details
	:return: 'app/results.html' page
	'''
	post = get_object_or_404(Property,pk=pk)
	id = Property.objects.get(pk=pk)
	pkey = id.pk
	pub_date = id.pub_date
	if request.method == 'POST':
		form = PropertyForm(request.POST, instance=instance)
	address = id.address
	beds = id.beds
	baths = id.baths
	listing_url = id.listing_url
	year_built = id.year_built
	county = id.county
	sqft = id.sqft
	schools = 'test'
	school_scores = '9,5,5'
	crime_level = id.crime_level
	nat_disasters = id.nat_disasters
	notes = id.notes
	cost_per_sqft = '$'+str(Property.cost_per_sqft_calc(id))
	taxes = '$'+str(int(Property.taxes_calc(id)/12))
	insurance = '$'+str(int(Property.insurance_calc(id)/12))
	hoa = '$'+str(int(id.hoa/12))
	maintenance = '$'+str(int(Property.maint_calc(id)/12))
	resign_fee = '$'+str(int(Property.resign_calc(id)/12))
	property_management_fee = '$'+str(id.property_management_fee)
	initial_improvements = '$'+str(id.initial_improvements)
	utilities = '$'+str(id.utilities)
	tenant_placement_fee = '$'+str(int(Property.tenant_place_calc(id)/12))
	rent = '$'+str(id.rent)
	curr_value = '$'+str(id.curr_value)
	interest_rate = str(id.interest_rate)+'%'
	closing_costs = '$'+str(id.closing_costs)
	vacancy = '$'+str(Property.vacancy_calc(id))
	oper_income = '$'+str(Property.oper_inc_calc(id))
	down_payment_percentage = str(id.down_payment_percentage)+str('%')
	down_payment = '$'+str(Property.down_payment_calc(id))
	total_mortgage = '$'+str(Property.total_mortgage_calc(id))
	mort_payment = '$'+str(Property.mort_payment_calc(id))
	init_cash_invest = '$'+str(Property.init_cash_invested_calc(id))
	oper_exp = '$'+str(Property.oper_exp_calc(id))
	net_oper_income = '$'+str(Property.net_oper_income_calc(id))
	cash_flow = '$'+str(Property.cash_flow_calc(id))
	oper_exp_ratio = Property.oper_exp_ratio_calc(id)*100
	oper_exp_ratio = str('%.1f' % oper_exp_ratio)+'%'
	debt_coverage_ratio = Property.debt_coverage_ratio_calc(id)
	cap_rate = Property.cap_rate(id)*100
	cap_rate = str('%.2f' % cap_rate)+'%'
	initial_market_value = '$'+str(id.curr_value)
	cash_on_cash = Property.cash_on_cash(id)*100
	cash_on_cash = str('%.2f' % cash_on_cash)+'%'
	rtv = Property.rtv_calc(id)*100
	rtv = str('%.2f' % rtv)+'%'
	id.save()
	template = loader.get_template('app/results.html')
	context = {
		'id': id,
		'pkey':pkey,
		'address':address,
		'taxes': taxes,
		'hoa': hoa,
		'rent': rent,
		'vacancy': vacancy,
		'oper_income': oper_income,
		'total_mortgage': total_mortgage,
		'down_payment_percentage': down_payment_percentage,
		'down_payment': down_payment,
		'curr_value': curr_value,
		'init_cash_invest': init_cash_invest,
		'oper_exp': oper_exp,
		'net_oper_income': net_oper_income,
		'cash_flow': cash_flow,
		'oper_exp_ratio': oper_exp_ratio,
		'debt_coverage_ratio': debt_coverage_ratio,
		'cap_rate': cap_rate,
		'initial_market_value': initial_market_value,
		'cash_on_cash': cash_on_cash,
		'interest_rate': interest_rate,
		'mort_payment': mort_payment,
		'sqft':sqft,
		'closing_costs':closing_costs,
		'initial_improvements':initial_improvements,
		'cost_per_sqft':cost_per_sqft,
		'insurance':insurance,
		'maintenance':maintenance,
		'property_management_fee':property_management_fee,
		'utilities':utilities,
		'tenant_placement_fee':tenant_placement_fee,
		'resign_fee':resign_fee,
		'notes':notes,
		'pub_date':pub_date,
		'rtv':rtv,
		'schools':schools,
		'school_scores':school_scores,
		'year_built': year_built,
		'county': county,
		'crime_level':crime_level,
		'nat_disasters':nat_disasters,
		'listing_url':listing_url,
		'beds':beds,
		'baths':baths
		}
	return HttpResponse(template.render(context))


def disclaimer(request):
	'''
	Specific paragraphs taken from Zillow.com terms of use
	:param request: HTTP Request
	:return: 'app/disclaimer.html' page
	'''
	return TemplateResponse(request, 'app/disclaimer.html')

