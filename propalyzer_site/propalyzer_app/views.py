import json
import re
from datetime import datetime
from decimal import Decimal

import requests
import logging
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.template.response import TemplateResponse
from django.utils import timezone

from .forms import AddressForm
from .forms import PropertyForm
from .models import Property
from .zillow_api import ZillowSetup

LOG = logging.getLogger(__name__)

@login_required
def address(request):
    """
    Renders the starting page for entering a property address
    :param request: HTTP Request
    :return: app/address.html page
    """

    researched_properties = Property.objects.filter(user=request.user)
    researched_property_list = researched_properties.order_by('-pub_date')
    owned_properties = Property.objects.filter(owned=True, user=request.user)
    owned_property_list = owned_properties.order_by('-pub_date')
    cash_flow_sum = 0
    for prop in owned_properties:
        cash_flow_sum = cash_flow_sum + prop.cash_flow
    form = AddressForm()
    if request.method == "POST":
        address_str = str(request.POST['address'])

        address_info = ZillowSetup(address_str)
        address_info.set_address()
        if address_info.error:
            return TemplateResponse(request, 'app/addressnotfound.html')

        address_info.set_zillow_url()
        if 'ConnectionError' in address_info.error:
            return TemplateResponse(request, 'app/connection_error.html')
        if 'AddressNotFound' in address_info.error:
            return TemplateResponse(request, 'app/addressnotfound.html')

        address_info.set_xml_data()

        # TODO Consider adding this to the zillow API class or having its own separate file to prevent combining
        # business logic within the view file
        areavibes_dict = get_areavibes_info(address_info.address_dict, address_info.lat, address_info.long)
        livability = areavibes_dict['livability']
        crime = areavibes_dict['crime']
        cost_of_living = areavibes_dict['cost_of_living']
        education = areavibes_dict['education']
        employment = areavibes_dict['employment']
        housing = areavibes_dict['housing']
        weather = areavibes_dict['weather']

        # Loggers
        LOG.debug('address_info.address_str --- {}'.format(address_info.address_str))
        LOG.debug('address_info.address_dict --- {}'.format(address_info.address_dict))
        LOG.debug('address_info.url --- {}'.format(address_info.url))
        LOG.debug('address_info.zillow_dict --- {}'.format(address_info.zillow_dict))
        LOG.debug('areavibes_dict--- {}'.format(areavibes_dict))

        # Property object create and commit to DB
        new_prop = Property(
            address=address_info.address_str, sqft=address_info.sqft, rent=address_info.rent_zest,
            rent_low=address_info.rent_low,
            rent_high=address_info.rent_high, curr_value=address_info.curr_value,
            value_low=address_info.value_low, value_high=address_info.value_high, year_built=address_info.year_built,
            interest_rate=4.75, county=address_info.county,
            crime_level='Unknown', nat_disasters='Unknown', lot_sqft=address_info.lot_sqft,
            neighborhood=address_info.neighborhood,
            listing_url=address_info.listing_url, beds=address_info.beds, baths=address_info.baths,
            livability=livability,
            crime=crime,
            cost_of_living=cost_of_living, education=education, employment=employment, housing=housing,
            weather=weather
        )
        try:
            new_prop.property_management_fee = int(.09 * int(new_prop.rent))
        except ValueError:
            new_prop.property_management_fee = 0
        new_prop.initial_market_value = new_prop.curr_value
        new_prop.insurance = int(1000)
        new_prop.taxes = int(2000)
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


def get_areavibes_url(ADDRESSDICT, lat, long):
    lat, long = str(lat), str(long)
    areavibes_url1 = 'http://www.areavibes.com/{}-{}/livability/'.format(
        ADDRESSDICT['PlaceName'],
        ADDRESSDICT['StateName'])
    areavibes_url2 = '?addr={}+{}+{}+{}&ll={}+{}'.format(
        ADDRESSDICT['AddressNumber'],
        ADDRESSDICT['StreetNamePreDirectional'],
        ADDRESSDICT['StreetName'],
        ADDRESSDICT['StreetNamePostType'],
        lat, long)
    areavibes_url = areavibes_url1 + areavibes_url2
    return areavibes_url


def get_areavibes_info(ADDRESSDICT, lat, long):
    """
    Method that generates the areavibes dictionary with areavibes information for a given address.
    :param ADDRESSDICT: Identified components of the property address (i.e. street name, city, zip code, etc.)
    :return: areavibes_dict - Dictionary that contains ratings sourced from areavibes.com based on a given address
    for the following categories:
        - Livability
        - Crime
        - Cost of Living
        - Education
        - Employment
        - Housing
        - Weather
    """
    url = get_areavibes_url(ADDRESSDICT, lat, long)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    info_block = soup.find_all('nav', class_='category-menu')
    try:
        result_string = info_block[0].get_text()
    except IndexError:
        result_string = 'Unknown'
    try:
        livability = int(re.findall('Livability(\d+)', result_string)[0])
    except IndexError:
        livability = 0
    try:
        crime = re.findall('Crime(.*?)Edu', result_string)[0]
    except IndexError:
        crime = 'Unknown'
    try:
        cost_of_living = re.findall('Living(.*?)Crime', result_string)[0]
    except IndexError:
        cost_of_living = 'Unknown'
    try:
        education = re.findall('Education(.*?)Empl', result_string)[0]
    except IndexError:
        education = 'Unknown'
    try:
        employment = re.findall('Employment(.*?)Hou', result_string)[0]
    except IndexError:
        employment = 'Unknown'
    try:
        housing = re.findall('Housing(.*?)Weather', result_string)[0]
    except IndexError:
        housing = 'Unknown'
    try:
        weather = re.findall('Weather(.*)$', result_string)[0].rstrip()
    except IndexError:
        weather = 'Unknown'
    areavibes_dict = {
        'livability': livability,
        'crime': crime,
        'cost_of_living': cost_of_living,
        'education': education,
        'employment': employment,
        'housing': housing,
        'weather': weather
    }
    return areavibes_dict


@login_required
def edit(request, pk):
    """
    Renders the 'app/edit.html' page for editing listing values
    :param request: HTTP Request
    :param pk: Primary Key - identifies the specific database record that corresponds with the listing details
    :return: 'app/edit.html' page
    """
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
    """
    Renders the results page which displays listing information, operating income/expense, cash flow, and
    investment ratios.
    :param request: HTTP request
    :param pk: Primary Key - identifies the specific database record that corresponds with the listing details
    :return: 'app/results.html' page
    """
    prop = Property.objects.get(pk=pk)
    context = {
        'id': prop,
        'pkey': prop.pk,
        'address': prop.address.replace("-", " "),
        'taxes': '$' + str(int(prop.taxes / 12)),
        'hoa': '$' + str(int(prop.hoa / 12)),
        'rent': '$' + str(prop.rent),
        'vacancy': '$' + str(prop.vacancy_calc),
        'oper_income': '$' + str(prop.oper_inc_calc),
        'total_mortgage': '$' + str(prop.total_mortgage_calc),
        'down_payment_percentage': str(prop.down_payment_percentage) + '%',
        'down_payment': '$' + str(prop.down_payment_calc),
        'curr_value': '$' + str(prop.curr_value),
        'init_cash_invest': '$' + str(prop.init_cash_invested_calc),
        'oper_exp': '$' + str(prop.oper_exp_calc),
        'net_oper_income': '$' + str(prop.net_oper_income_calc),
        'cap_rate': '{0:.1f}%'.format(prop.cap_rate() * 100),
        'initial_market_value': '$' + str(prop.curr_value),
        'interest_rate': str(prop.interest_rate) + '%',
        'mort_payment': '$' + str(prop.mort_payment_calc),
        'sqft': prop.sqft,
        'closing_costs': '$' + str(prop.closing_costs),
        'initial_improvements': '$' + str(prop.initial_improvements),
        'cost_per_sqft': '$' + str(prop.cost_per_sqft_calc),
        'insurance': '$' + str(int(prop.insurance / 12)),
        'maintenance': '$' + str(int(prop.maint_calc / 12)),
        'property_management_fee': '$' + str(prop.property_management_fee),
        'utilities': '$' + str(prop.utilities),
        'tenant_placement_fee': '$' + str(int(prop.tenant_place_calc / 12)),
        'resign_fee': '$' + str(int(prop.resign_calc / 12)),
        'notes': prop.notes,
        'pub_date': prop.pub_date,
        'rtv': '{0:.2f}%'.format(prop.rtv_calc * 100),
        'cash_flow': '$' + str(prop.cash_flow_calc),
        'oper_exp_ratio': '{0:.1f}'.format(prop.oper_exp_ratio_calc * 100) + '%',
        'debt_coverage_ratio': prop.debt_coverage_ratio_calc,
        'cash_on_cash': '{0:.2f}%'.format(prop.cash_on_cash() * 100),
        'schools': 'Unknown',
        'school_scores': '0,0,0',
        'year_built': prop.year_built,
        'county': prop.county,
        'crime_level': prop.crime_level,
        'nat_disasters': prop.nat_disasters,
        'listing_url': prop.listing_url,
        'beds': prop.beds,
        'baths': prop.baths,
        'livability': prop.livability,
        'crime': prop.crime,
        'cost_of_living': prop.cost_of_living,
        'education': prop.education,
        'employment': prop.employment,
        'housing': prop.housing,
        'weather': prop.weather
    }
    prop.save()
    template = loader.get_template('app/results.html')
    return HttpResponse(template.render(context))


def disclaimer(request):
    """
    Renders the disclaimer page with specific paragraphs taken from Zillow.com terms of use
    :param request: HTTP Request
    :return: 'app/disclaimer.html' page
    """
    return TemplateResponse(request, 'app/disclaimer.html')
