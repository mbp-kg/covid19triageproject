# -*- coding: utf-8 -*-
from braces.views import MultiplePermissionsRequiredMixin
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.messages.api import error
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import ModelFormMixin
from django.views.generic.list import ListView
from workinghours.api import is_open

from ..forms import AssessmentForm
from ..models import Assessment
from ..models import AssessmentLog
from ..scoring import calculate_score


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


class AssessmentView(
    MultiplePermissionsRequiredMixin, ModelFormMixin, DetailView
):
    """
    Display an Assessment
    """

    extra_context = {
        "pagetitle": _("Assessment"),
        "title": _("Assessment"),
    }
    form_class = AssessmentForm
    model = Assessment
    permissions = {
        "all": (
            "covid19triage.view_assessment",
            "covid19triage.view_patient",
            "covid19triage.view_patientfactors",
        ),
    }
    pk_url_kwarg = "pk"
    template_name = "covid19triage/doctors/assessment.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = _("Assessment for {patient}").format(
            patient=str(self.object.patientfactors.patient)
        )
        context["pagetitle"] = context["title"] = title
        return context

    def form_invalid(self, form):
        if "version" in form.errors:
            for verror in form.errors.get("version"):
                error(self.request, verror)
        return super().form_invalid(form)

    def form_valid(self, form):
        oldassessment = Assessment.objects.get(pk=int(self.kwargs.get("pk")))
        newassessment = form.save(commit=False)
        if oldassessment.version == newassessment.version:
            newassessment.save()
        loglines = []
        if oldassessment.owner != newassessment.owner:
            loglines.append(
                "{user} changed the owner from {oldowner} to {newowner}".format(
                    user=self.request.user.username,
                    oldowner=oldassessment.owner,
                    newowner=newassessment.owner,
                )
            )
        if oldassessment.status != newassessment.status:
            loglines.append(
                "{user} changed the assessment status from {oldstatus} to {newstatus}".format(
                    user=self.request.user.username,
                    oldstatus=oldassessment.status,
                    newstatus=newassessment.status,
                )
            )
        if loglines:
            alog = AssessmentLog()
            alog.assessment = newassessment
            alog.user = self.request.user
            alog.comments = "\n".join(loglines)
            alog.save()
        return redirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class AssessmentListView(MultiplePermissionsRequiredMixin, ListView):
    filter = "active"
    model = Assessment
    permissions = {
        "all": (
            "covid19triage.view_assessment",
            "covid19triage.view_patient",
            "covid19triage.view_patientfactors",
        ),
    }
    template_name = "covid19triage/doctors/index.html"
    titlebyfilter = {
        "active": _("Active Assessments"),
        "my": _("My Assessments"),
        "completed": _("Completed Assessments"),
        "unclaimed": _("Unclaimed Assessments"),
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = self.titlebyfilter.get(kwargs.get("filter"), _("Assessments"))
        context["pagetitle"] = title
        context["title"] = title
        return context

    def get_queryset(self):
        if self.filter == "active":
            qs = (
                Assessment.objects.exclude(status=Assessment.Status.TESTING)
                .exclude(status=Assessment.Status.NOFURTHERACTION)
                .exclude(status=Assessment.Status.REFERREDFORTREATMENT)
            )
        elif self.filter == "completed":
            qs = Assessment.objects.filter(
                status__in=[
                    Assessment.Status.TESTING,
                    Assessment.Status.NOFURTHERACTION,
                    Assessment.Status.REFERREDFORTREATMENT,
                ]
            )
        elif self.filter == "my":
            qs = Assessment.objects.filter(owner=self.request.user)
        elif self.filter == "myactive":
            qs = Assessment.objects.filter(owner=self.request.user).exclude(
                status__in=[
                    Assessment.Status.TESTING,
                    Assessment.Status.NOFURTHERACTION,
                    Assessment.Status.REFERREDFORTREATMENT,
                ]
            )
        elif self.filter == "unclaimed":
            qs = Assessment.objects.filter(owner=None)
        else:
            qs = Assessment.objects.all()
        return qs


# Hacky update for scores, since the Fake model objects cannot be used to
# calculate scores in migrations.
@user_passes_test(lambda u: u.is_superuser)
def updatescores(request):
    for a in Assessment.objects.filter(score=-1):
        pf = a.patientfactors
        p = pf.patient
        s = calculate_score(p, pf)
        a.score = s
        a.version += 1
        a.save()
    return HttpResponse("OK")
