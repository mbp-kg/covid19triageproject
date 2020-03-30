# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import FormView

from .forms import ContactInformationForm
from .forms import PatientFactorsForm
from .forms import PatientInformationForm

from .models import Patient
from .models import PatientFactors
from .models import Risk
from .models import Symptom
from .models import get_current_pfv

def _make_title(pagetitle: str) -> str:
    prefix = _("COVID-19 Triage")
    return "{} — {}".format(prefix, pagetitle)


def index(request):
    pagetitle = _("Language")
    return render(request, "covid19triage/index.html", {
        "pagetitle": _make_title(pagetitle),
        "title": pagetitle,
    })


def result(request):
    return render(request, "covid19triage/result.html", {})


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
        self.request.session["contactinfoid"] = contactinfo.pk
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

    def form_valid(self, form):
        patient = Patient.objects.get(pk=self.request.session.get("patientid"))
        version = get_current_pfv()
        patientfactors = form.save(commit=False)
        patientfactors.patient = patient
        patientfactors.version = version
        patientfactors.save()
        form.save_m2m()
        self.request.session["patientfactorsid"] = patientfactors.pk
        return redirect("covid19triage:result")


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
        patient = form.save()
        self.request.session["patientid"] = patient.pk
        return redirect("covid19triage:patientfactors")
