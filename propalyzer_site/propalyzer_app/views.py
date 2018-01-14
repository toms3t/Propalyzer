from datetime import datetime
import logging
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.utils import timezone
from .forms import AddressForm
from .forms import PropertyForm
from .property import PropSetup

# Globals
LOG = logging.getLogger(__name__)
ADDRESS = ''
PROP = PropSetup('')


def address(request):
    """
    Renders the starting page for entering a property address
    :param request: HTTP Request
    :return: app/address.html page
    """

    if request.method == "POST":
        address_str = str(request.POST['text_input'])
        PROP = PropSetup(address_str)
        PROP.set_address()
        if PROP.error:
            return TemplateResponse(request, 'app/addressnotfound.html')

        PROP.set_zillow_url()
        if 'ConnectionError' in PROP.error:
            return TemplateResponse(request, 'app/connection_error.html')
        if 'AddressNotFound' in PROP.error:
            return TemplateResponse(request, 'app/addressnotfound.html')

        PROP.set_xml_data()
        PROP.set_areavibes_info()

        # Loggers
        LOG.debug('PROP.address --- {}'.format(PROP.address))
        LOG.debug('PROP.address_dict --- {}'.format(PROP.address_dict))
        LOG.debug('PROP.url --- {}'.format(PROP.url))
        LOG.debug('PROP.zillow_dict --- {}'.format(PROP.zillow_dict))
        LOG.debug('areavibes_dict--- {}'.format(PROP.areavibes_dict))

        try:
            PROP.prop_management_fee = int(.09 * int(PROP.rent))
        except ValueError:
            PROP.prop_management_fee = 0
        PROP.initial_market_value = PROP.curr_value
        PROP.initial_improvements = 0
        PROP.insurance = 1000
        PROP.maintenance = 800
        PROP.taxes = 1500
        PROP.hoa = 0
        PROP.utilities = 0
        PROP.interest_rate = 4.75
        PROP.down_payment_percentage = 25
        PROP.down_payment = int(PROP.curr_value) * (PROP.down_payment_percentage / 100.0)
        PROP.closing_costs = int(.03 * int(PROP.curr_value))

        request.session['PROP'] = PROP.__dict__
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
        PROP = request.session.get('PROP')

        PROP_list = ['sqft', 'curr_value', 'rent', 'down_payment_percentage', 'interest_rate', 'closing_costs',
                     'initial_improvements', 'hoa', 'insurance', 'taxes', 'utilities', 'maintenance',
                     'prop_management_fee', 'tenant_placement_fee', 'resign_fee', 'schools', 'county',
                     'year_built', 'notes']
        for key in PROP_list:
            PROP[key] = form.data[key]

        request.session['PROP'] = PROP
        if form.is_valid():
            return redirect('results')
    else:
        PROP = request.session.get('PROP')
        form = PropertyForm(initial={key: PROP[key] for key in PROP.keys()})

    return render(request, 'app/edit.html', {'form': form})


def results(request):
    """
    Renders the results page which displays listing information, operating income/expense, cash flow, and
    investment ratios.
    :param c: HTTP request
    :return: 'app/results.html' page
    """
    PROP_data = request.session.get('PROP')
    PROP=PropSetup(PROP_data['address'])
    for key in PROP_data.keys():
        PROP.__dict__[key] = PROP_data[key]

    context = {
        'address': PROP.address,
        'taxes': '$' + str(int(int(PROP.taxes) / 12)),
        'hoa': '$' + str(int(int(PROP.hoa) / 12)),
        'rent': '$' + str(PROP.rent),
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
        'insurance': '$' + str(int(PROP.insurance) / 12),
        'maintenance': '$' + str(int(PROP.maint_calc) / 12),
        'prop_management_fee': '$' + str(PROP.prop_management_fee),
        'utilities': '$' + str(PROP.utilities),
        'tenant_placement_fee': '$' + str(int(PROP.tenant_place_calc) / 12),
        'resign_fee': '$' + str(int(PROP.resign_calc) / 12),
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

    request.session['PROP'] = PROP.__dict__
    return render(request, 'app/results.html', context)


def disclaimer(request):
    """
    Renders the disclaimer page with specific paragraphs taken from Zillow.com terms of use
    :param request: HTTP Request
    :return: 'app/disclaimer.html' page
    """
    return TemplateResponse(request, 'app/disclaimer.html')
