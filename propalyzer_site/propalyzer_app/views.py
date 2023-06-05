from datetime import datetime
import logging
import os
import requests
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
# from .pdf_render import Render
from .forms import AddressForm
from .forms import PropertyForm
from .property import PropSetup
from .context_data import ContextData, mk_int

LOG = logging.getLogger(__name__)

try:
    zillow_api_key = os.environ["zillow_api_key"]
except KeyError:
    zillow_api_key = None


def _validate_api_key():
    """
    Function to validate zillow API key. This determines whether actual data is returned from Zillow or if fictional data is shown on the app.
    :return: Bool
    """
    pub_record_url = f"https://api.bridgedataoutput.com/api/v2/pub/assessments?"
    pub_record_url += f"access_token={zillow_api_key}&zpid=16128477&sortBy=year"
    resp = requests.get(pub_record_url)
    if str(resp.status_code) == "200":
        return True


def address(request):
    """
    Renders the starting page for entering a property address
    :param request: HTTP Request
    :return: app/address.html page
    """

    if request.method == "POST":
        zillow_api_key_valid = _validate_api_key()
        if not zillow_api_key_valid:
            address_str = str(request.POST["text_input"])
        prop = PropSetup(address_str)
        prop.get_info(zillow_api_key_valid)
        if prop.error == "ConnectionError":
            return TemplateResponse(request, "app/connection_error.html")
        if prop.error == "AddressNotFound":
            return TemplateResponse(request, "app/addressnotfound.html")
        prop.prop_management_fee = int(prop.rent * 0.09)
        prop.closing_costs = int(prop.zestimate * 0.03)
        prop.taxes = int(prop.taxes)

        request.session["prop"] = prop.dict_from_class()
        return redirect("edit")
    else:
        context = {
            "title": "Home Page",
            "year": datetime.now().year,
            "form": AddressForm(),
        }
        return TemplateResponse(request, "app/address.html", context)


def edit(request):
    """
    Renders the 'app/edit.html' page for editing listing values
    :param request: HTTP Request
    :return: 'app/edit.html' page
    """
    if request.method == "POST":
        form = PropertyForm(request.POST)
        prop = request.session.get("prop")

        prop_list = [
            "sqft",
            "zestimate",
            "rent",
            "down_payment_percentage",
            "interest_rate",
            "closing_costs",
            "initial_improvements",
            "hoa",
            "insurance",
            "taxes",
            "utilities",
            "maintenance",
            "prop_management_fee",
            "tenant_placement_fee",
            "resign_fee",
            "county",
            "year_built",
            "notes",
        ]

        for key in prop_list:
            prop[key] = form.data[key]
        prop['down_payment'] = int(
            (float(prop['down_payment_percentage']) * mk_int(prop['zestimate'])) / 100
        )

        request.session["prop"] = prop
        if form.is_valid():
            return redirect("results")
    else:
        prop = request.session.get("prop")
        form = PropertyForm(initial={key: prop[key] for key in prop.keys()})

    return render(request, "app/edit.html", {"form": form})


def results(request):
    """
    Renders the results page which displays property information (general and financial metrics)
    :param: HTTP request
    :return: 'app/results.html' page
    """

    prop_data = request.session.get("prop")

    prop = ContextData()
    context = prop.set_data(prop_data)
    request.session["PROP"] = prop.__dict__
    return render(request, "app/results.html", context)


# def pdf(request):
#     prop_data = request.session.get("prop")

#     prop = ContextData()
#     context = prop.set_data(prop_data)

#     return Render.render("app/results.html", context)


def disclaimer(request):
    """
    Renders the disclaimer page with specific paragraphs taken from Zillow.com terms of use
    :param request: HTTP Request
    :return: 'app/disclaimer.html' page
    """
    return TemplateResponse(request, "app/disclaimer.html")
