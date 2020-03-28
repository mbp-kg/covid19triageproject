# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext, gettext_lazy as _
from django.utils.translation import pgettext, pgettext_lazy
from django.views.generic.edit import FormView

from .forms import ContactInformationForm
from .forms import PatientFactorsForm
from .forms import PatientInformationForm


def _make_title(pagetitle: str) -> str:
    prefix = pgettext_lazy("page title", "COVID-19 Triage")
    return "{} — {}".format(prefix, pagetitle)


def index(request):
    pagetitle = pgettext_lazy("page title", "Language")
    pageheader = pgettext_lazy("page header", "Language")
    return render(request, "covid19triage/index.html", {
        "pagetitle": _make_title(pagetitle),
        "title": pageheader,
    })


class ContactInformationView(FormView):
    """
    Display the contact information form
    """
    pagetitle = pgettext_lazy("page title", "Contact Information")
    pageheader = pgettext_lazy("page header", "Contact Information")
    extra_context = {
        "pagetitle": _make_title(pagetitle),
        "title": pageheader,
    }
    form_class = ContactInformationForm
    template_name = "covid19triage/contactinfo.html"


class PatientFactorsView(FormView):
    """
    Display the patient factors form
    """
    pagetitle = pgettext_lazy("page title", "Symptoms and Risk Factors")
    pageheader = pgettext_lazy("page header", "Symptoms and Risk Factors")
    extra_context = {
        "pagetitle": _make_title(pagetitle),
        "title": pageheader,
    }
    form_class = PatientFactorsForm
    template_name = "covid19triage/patientfactors.html"


class PatientInformationView(FormView):
    """
    Display the patient information form
    """
    pagetitle = pgettext_lazy("page title", "Patient Information")
    pageheader = pgettext_lazy("page header", "Patient Information")
    extra_context = {
        "pagetitle": _make_title(pagetitle),
        "title": pageheader,
    }
    form_class = PatientInformationForm
    template_name = "covid19triage/patientinfo.html"
