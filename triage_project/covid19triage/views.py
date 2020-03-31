# -*- coding: utf-8 -*-
from django.contrib.messages.api import info
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import FormView
from workinghours.api import is_open

from .forms import ContactInformationForm
from .forms import PatientFactorsForm
from .forms import PatientInformationForm

from .models import Patient
from .models import PatientFactors
from .models import Risk
from .models import Symptom
from .models import get_current_pfv

from .scoring import calculate_score


def _make_pagetitle(pagetitle: str) -> str:
    prefix = _("COVID-19 Triage")
    return "{} — {}".format(prefix, pagetitle)


def index(request):
    if is_open(timezone.now()):
        info(request, _("Eldik Family Medicine Clinic is currently open."))
    else:
        info(request, _("Eldik Family Medicine Clinic is currently closed."))
    title = _("Language")
    return render(request, "covid19triage/index.html", {
        "pagetitle": _make_pagetitle(title),
        "title": title,
    })


def intro(request):
    title = _("Welcome")
    context = {
        "pagetitle": _make_pagetitle(title),
        "title": title,
    }
    return render(request, "covid19triage/intro.html", context)


def result(request):
    contactinfoid = request.session.get("contactinfoid")
    if contactinfoid is None:
        return redirect("covid19triage:contactinfo")
    patientid = request.session.get("patientid")
    if patientid is None:
        return redirect("covid19triage:patientinfo")
    patientfactorsid = request.session.get("patientfactorsid")
    if patientfactorsid is None:
        return redirect("covid19triage:patientfactors")

    patient = Patient.objects.get(pk=patientid)
    patientfactors = PatientFactors.objects.get(pk=patientfactorsid)
    score = calculate_score(patient, patientfactors)

    context = {
        "open": is_open(timezone.now()),
        "pagetitle": _make_pagetitle("Result"),
        "score": score,
        "title": title,
    }

    return render(request, "covid19triage/result.html", context)


class ContactInformationView(FormView):
    """
    Display the contact information form
    """
    title = _("Contact Information")
    extra_context = {
        "pagetitle": _make_pagetitle(title),
        "title": title,
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
    title = _("Symptoms and Risk Factors")
    extra_context = {
        "pagetitle": _make_pagetitle(title),
        "title": title,
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
    title = _("Patient Information")
    extra_context = {
        "pagetitle": _make_pagetitle(title),
        "title": title,
    }
    form_class = PatientInformationForm
    template_name = "covid19triage/patientinfo.html"

    def form_valid(self, form):
        patient = form.save()
        self.request.session["patientid"] = patient.pk
        return redirect("covid19triage:patientfactors")
