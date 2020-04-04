# -*- coding: utf-8 -*-
from braces.views import MultiplePermissionsRequiredMixin
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic.list import ListView
from workinghours.api import is_open

from ..models import PatientFactors


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect(request.GET.get("next", "/no_next"))
    context = {
        "next": request.POST.get("next", request.GET.get("next")),
        "title": _("Log in"),
        "username": request.user.get_username(),
    }
    defaults = {
        "extra_context": context,
        "authentication_form": AdminAuthenticationForm,
        "template_name": "covid19triage/login.html",
    }
    return LoginView.as_view(**defaults)(request)


def logout(request):
    auth_logout(request)
    defaults = {
        "template_name": "covid19triage/loggedout.html",
    }
    return LogoutView.as_view(**defaults)(request)


class PatientAssessmentsView(MultiplePermissionsRequiredMixin, ListView):
    model = PatientFactors
    permissions = {
        "all": (
            "covid19triage.view_patient",
            "covid19triage.view_patientfactors",
        ),
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = _("Patient Assessments")
        context["title"] = title
        return context
