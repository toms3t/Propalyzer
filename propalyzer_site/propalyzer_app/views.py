from datetime import datetime
import logging
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.utils import timezone
from .pdf_render import Render
from .forms import AddressForm
from .forms import PropertyForm
from .property import PropSetup
from .context_data import ContextData

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
        prop.get_info()
        if prop.error:
            return TemplateResponse(request, 'app/addressnotfound.html')

        if 'ConnectionError' in prop.error:
            return TemplateResponse(request, 'app/connection_error.html')
        if 'AddressNotFound' in prop.error:
            return TemplateResponse(request, 'app/addressnotfound.html')

        # Loggers
        LOG.debug('prop.address --- {}'.format(prop.address))
        LOG.debug('prop.address_dict --- {}'.format(prop.address_dict))
        LOG.debug('prop.url --- {}'.format(prop.url))
        LOG.debug('prop.zillow_dict --- {}'.format(prop.zillow_dict))
        LOG.debug('areavibes_dict--- {}'.format(prop.areavibes_dict))

        request.session['prop'] = prop.dict_from_class()
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

    prop = ContextData()
    context = prop.set_data(prop_data)
    request.session['PROP'] = prop.__dict__
    return render(request, 'app/results.html', context)


def pdf(request):
    prop_data = request.session.get('prop')

    prop = ContextData()
    context = prop.set_data(prop_data)

    return Render.render('app/results.html', context)


def disclaimer(request):
    """
    Renders the disclaimer page with specific paragraphs taken from Zillow.com terms of use
    :param request: HTTP Request
    :return: 'app/disclaimer.html' page
    """
    return TemplateResponse(request, 'app/disclaimer.html')
