from datetime import datetime
import logging
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.utils import timezone
from .forms import AddressForm
from .forms import PropertyForm
from .property import PropSetup
from .greatschools import GreatSchools

LOG = logging.getLogger(__name__)


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
        LOG.debug('prop.address --- {}'.format(prop.address))
        LOG.debug('prop.address_dict --- {}'.format(prop.address_dict))
        LOG.debug('prop.url --- {}'.format(prop.url))
        LOG.debug('prop.zillow_dict --- {}'.format(prop.zillow_dict))
        LOG.debug('areavibes_dict--- {}'.format(prop.areavibes_dict))

        try:
            prop.prop_management_fee = int(.09 * int(prop.rent))
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

        request.session['prop'] = prop.__dict__
        return redirect('edit')
    else:
        context = {
            'title': 'Home Page',
            'year': datetime.now().year,
            'form': AddressForm(),
        }
        return TemplateResponse(request, 'app/address.html', context)


def edit(request):
    """
    Renders the 'app/edit.html' page for editing listing values
    :param request: HTTP Request
    :return: 'app/edit.html' page
    """
    if request.method == "POST":
        form = PropertyForm(request.POST)
        prop = request.session.get('prop')

        prop_list = ['sqft', 'curr_value', 'rent', 'down_payment_percentage', 'interest_rate', 'closing_costs',
                     'initial_improvements', 'hoa', 'insurance', 'taxes', 'utilities', 'maintenance',
                     'prop_management_fee', 'tenant_placement_fee', 'resign_fee', 'county',
                     'year_built', 'notes']
        for key in prop_list:
            prop[key] = form.data[key]

        request.session['prop'] = prop
        if form.is_valid():
            return redirect('results')
    else:
        prop = request.session.get('prop')
        form = PropertyForm(initial={key: prop[key] for key in prop.keys()})

    return render(request, 'app/edit.html', {'form': form})


def results(request):
    """
    Renders the results page which displays property information (general, schools, and financial metrics)
    :param: HTTP request
    :return: 'app/results.html' page
    """

    prop_data = request.session.get('prop')
    schools = GreatSchools(
        prop_data['address'], prop_data['city'], prop_data['state'], prop_data['zip_code'], prop_data['county'])
    schools.set_greatschool_urls()
    if schools.api_key and schools.DAILY_API_CALL_COUNT <= 2950:
        for url in schools.urls:
            schools.get_greatschool_xml(url)

    else:
        schools.elem_school = 'Unknown'
        schools.mid_school = 'Unknown'
        schools.high_school = 'Unknown'
    prop = PropSetup(prop_data['address'])
    for key in prop_data.keys():
        prop.__dict__[key] = prop_data[key]

    context = {
        'address': prop.address,
        'taxes': '$' + str(int(int(prop.taxes) / 12)),
        'hoa': '$' + str(int(int(prop.hoa) / 12)),
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
        'cap_rate': '{0:.1f}%'.format(prop.cap_rate_calc * 100),
        'initial_market_value': '$' + str(prop.curr_value),
        'interest_rate': str(prop.interest_rate) + '%',
        'mort_payment': '$' + str(prop.mort_payment_calc),
        'sqft': prop.sqft,
        'closing_costs': '$' + str(prop.closing_costs),
        'initial_improvements': '$' + str(prop.initial_improvements),
        'cost_per_sqft': '$' + str(prop.cost_per_sqft_calc),
        'insurance': '$' + str(int(int(prop.insurance) / 12)),
        'maintenance': '$' + str(int(int(prop.maint_calc) / 12)),
        'prop_management_fee': '$' + str(prop.prop_management_fee),
        'utilities': '$' + str(prop.utilities),
        'tenant_placement_fee': '$' + str(int(int(prop.tenant_place_calc) / 12)),
        'resign_fee': '$' + str(int(int(prop.resign_calc) / 12)),
        'notes': prop.notes,
        'pub_date': timezone.now,
        'rtv': '{0:.2f}%'.format(prop.rtv_calc * 100),
        'cash_flow': '$' + str(prop.cash_flow_calc),
        'oper_exp_ratio': '{0:.1f}'.format(prop.oper_exp_ratio_calc * 100) + '%',
        'debt_coverage_ratio': prop.debt_coverage_ratio_calc,
        'cash_on_cash': '{0:.2f}%'.format(prop.cash_on_cash_calc * 100),
        'elem_school': schools.elem_school,
        'elem_school_score': schools.elem_school_score,
        'mid_school': schools.mid_school,
        'mid_school_score': schools.mid_school_score,
        'high_school': schools.high_school,
        'high_school_score': schools.high_school_score,
        'year_built': prop.year_built,
        'county': prop.county,
        'nat_disasters': 'Unknown',
        'listing_url': prop.listing_url,
        'beds': prop.beds,
        'baths': prop.baths,
        'livability': prop.areavibes_dict['livability'],
        'crime': prop.areavibes_dict['crime'],
        'cost_of_living': prop.areavibes_dict['cost_of_living'],
        'education': prop.areavibes_dict['education'],
        'employment': prop.areavibes_dict['employment'],
        'housing': prop.areavibes_dict['housing'],
        'weather': prop.areavibes_dict['weather']
    }

    request.session['PROP'] = prop.__dict__
    return render(request, 'app/results.html', context)


def disclaimer(request):
    """
    Renders the disclaimer page with specific paragraphs taken from Zillow.com terms of use
    :param request: HTTP Request
    :return: 'app/disclaimer.html' page
    """
    return TemplateResponse(request, 'app/disclaimer.html')
