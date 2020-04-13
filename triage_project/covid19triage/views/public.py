# -*- coding: utf-8 -*-
from django.contrib.messages.api import info
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic.edit import FormView
from workinghours.api import is_open

from ..forms import ContactInformationForm
from ..forms import PatientFactorsForm
from ..forms import PatientInformationForm
from ..forms import ProposedDateTimeForm

from ..models import Assessment
from ..models import ContactPerson
from ..models import Patient
from ..models import PatientFactors
from ..models import ProposedDateTime
from ..models import Risk
from ..models import Symptom
from ..models import get_current_pfv

from ..scoring import calculate_score


def _make_pagetitle(pagetitle: str) -> str:
    prefix = _("COVID-19 Assessment")
    return "{} — {}".format(prefix, pagetitle)


def index(request):
    if is_open(timezone.now()):
        info(request, _("Eldik Family Medicine Clinic is currently open."))
    else:
        info(request, _("Eldik Family Medicine Clinic is currently closed."))
    title = _("Language")
    return render(
        request,
        "covid19triage/index.html",
        {"pagetitle": _make_pagetitle(title), "title": title,},
    )


def intro(request):
    title = _("Welcome")
    context = {
        "pagetitle": _make_pagetitle(title),
        "title": title,
    }
    return render(request, "covid19triage/intro.html", context)


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
        "secondperson": False,
        "title": title,
    }
    form_class = PatientFactorsForm
    template_name = "covid19triage/patientfactors.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        contactinfoid = self.request.session.get("contactinfoid")
        contactinfo = ContactPerson.objects.get(pk=contactinfoid)
        if contactinfo.forwhom == ContactPerson.ForWhom.SELF:
            context["secondperson"] = True

        patientid = self.request.session.get("patientid")
        patient = Patient.objects.get(pk=patientid)
        if patient.gender == Patient.MedicalGender.FEMALE:
            context["askaboutpregnancy"] = True

        return context

    def form_valid(self, form):
        patient = Patient.objects.get(pk=self.request.session.get("patientid"))
        version = get_current_pfv()
        patientfactors = form.save(commit=False)
        patientfactors.patient = patient
        patientfactors.version = version
        patientfactors.save()
        form.save_m2m()
        self.request.session["patientfactorsid"] = patientfactors.pk

        assessment = Assessment()
        assessment.patientfactors = patientfactors
        assessment.score = calculate_score(patient, patientfactors)
        assessment.save()
        self.request.session["assessmentid"] = assessment.pk

        return redirect("covid19triage:result")


class PatientInformationView(FormView):
    """
    Display the patient information form
    """

    title = _("Patient Information")
    extra_context = {
        "pagetitle": _make_pagetitle(title),
        "secondperson": False,
        "title": title,
    }
    form_class = PatientInformationForm
    template_name = "covid19triage/patientinfo.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contactinfoid = self.request.session.get("contactinfoid")
        contactperson = ContactPerson.objects.get(pk=contactinfoid)
        if contactperson.forwhom == ContactPerson.ForWhom.SELF:
            context["secondperson"] = True
        return context

    def get_initial(self):
        initial = super().get_initial()
        contactinfoid = self.request.session.get("contactinfoid")
        if contactinfoid:
            contactperson = ContactPerson.objects.get(pk=contactinfoid)
            if (
                contactperson
                and contactperson.forwhom == ContactPerson.ForWhom.SELF
            ):
                initial["firstname"] = contactperson.firstname
                initial["lastname"] = contactperson.lastname
        return initial

    def form_valid(self, form):
        contactinfoid = self.request.session.get("contactinfoid")
        contactperson = ContactPerson.objects.get(pk=contactinfoid)

        patient = form.save(commit=False)
        patient.contactperson = contactperson
        patient.save()

        self.request.session["patientid"] = patient.pk
        return redirect("covid19triage:patientfactors")


class ProposedDateTimeView(FormView):
    "Allow the contact person to propose a date and time for a consultation"

    title = _("Result")
    extra_context = {
        "pagetitle": _make_pagetitle(title),
        "title": title,
    }
    form_class = ProposedDateTimeForm
    template_name = "covid19triage/result.html"

    def form_valid(self, form):
        assessmentid = self.request.session.get("assessmentid")
        assessment = Assessment.objects.get(pk=assessmentid)
        proposeddatetime = form.save(commit=False)
        proposeddatetime.assessment = assessment
        proposeddatetime.save()
        self.request.session["proposeddatetimeid"] = proposeddatetime.pk

        return redirect("covid19triage:result")

    def get_context_data(self, **kwargs):
        _add_open_closed_message(self.request)
        context = super().get_context_data(**kwargs)
        assessmentid = self.request.session.get("assessmentid")
        assessment = Assessment.objects.get(pk=assessmentid)
        context["score"] = assessment.score
        return context


class ResultView(View):
    "Show the result and, possibly, a form for suggesting a date and time"

    def get(self, request, *args, **kwargs):
        title = _("Result")
        contactinfoid = request.session.get("contactinfoid")
        if contactinfoid is None:
            return redirect("covid19triage:contactinfo")
        patientid = request.session.get("patientid")
        if patientid is None:
            return redirect("covid19triage:patientinfo")
        patientfactorsid = request.session.get("patientfactorsid")
        if patientfactorsid is None:
            return redirect("covid19triage:patientfactors")
        assessmentid = request.session.get("assessmentid")
        if assessmentid is None:
            patient = Patient.objects.get(pk=patientid)
            patientfactors = PatientFactors.objects.get(pk=patientfactorsid)
            score = calculate_score(patient, patientfactors)
        else:
            assessment = Assessment.objects.get(pk=assessmentid)
            score = assessment.score
        proposeddatetimeid = request.session.get("proposeddatetimeid")
        if proposeddatetimeid is not None:
            info(
                self.request,
                _("Your suggested date and time have been saved."),
            )
            proposeddatetime = ProposedDateTime.objects.get(
                pk=proposeddatetimeid
            )
            form = ProposedDateTimeForm(instance=proposeddatetime)
        else:
            form = ProposedDateTimeForm()

        context = {
            "form": form,
            "pagetitle": _make_pagetitle(title),
            "score": score,
            "title": title,
        }

        return render(request, "covid19triage/result.html", context)

    def post(self, request, *args, **kwargs):
        view = ProposedDateTimeView.as_view()
        return view(request, *args, **kwargs)
