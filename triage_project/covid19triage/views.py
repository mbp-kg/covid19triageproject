# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext, gettext_lazy as _
from django.utils.translation import pgettext, pgettext_lazy
from django.views.generic.edit import FormView

from .forms import ContactInformationForm


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
