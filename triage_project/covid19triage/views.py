# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import FormView

from .forms import ContactInformationForm
from .forms import PatientFactorsForm
from .forms import PatientInformationForm


def _make_title(pagetitle: str) -> str:
    prefix = _("COVID-19 Triage")
    return "{} — {}".format(prefix, pagetitle)


def index(request):
    pagetitle = _("Language")
    return render(request, "covid19triage/index.html", {
        "pagetitle": _make_title(pagetitle),
        "title": pagetitle,
    })


class ContactInformationView(FormView):
    """
    Display the contact information form
    """
    pagetitle = _("Contact Information")
    extra_context = {
        "pagetitle": _make_title(pagetitle),
        "title": pagetitle,
    }
    form_class = ContactInformationForm
    template_name = "covid19triage/contactinfo.html"

    def form_valid(self, form):
        contactinfo = form.save()
        self.request.session["contactinfo"] = contactinfo.pk
        return redirect("covid19triage:patientinfo")

class PatientFactorsView(FormView):
    """
    Display the patient factors form
    """
    pagetitle = _("Symptoms and Risk Factors")
    extra_context = {
        "pagetitle": _make_title(pagetitle),
        "title": pagetitle,
    }
    form_class = PatientFactorsForm
    template_name = "covid19triage/patientfactors.html"


class PatientInformationView(FormView):
    """
    Display the patient information form
    """
    pagetitle = _("Patient Information")
    extra_context = {
        "pagetitle": _make_title(pagetitle),
        "title": pagetitle,
    }
    form_class = PatientInformationForm
    template_name = "covid19triage/patientinfo.html"

    def form_valid(self, form):
        patientinfo = form.save()
        self.request.session["patientinfo"] = patientinfo.pk
        return redirect("covid19triage:patientfactors")
