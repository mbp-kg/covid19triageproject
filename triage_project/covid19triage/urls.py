"""triage_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import doctors
from .views import public


urlpatterns = [
    path("", public.index, name="index"),
    path(
        _("contactinfo"),
        public.ContactInformationView.as_view(),
        name="contactinfo",
    ),
    path(
        _("doctors"),
        doctors.AssessmentListView.as_view(),
        name="doctorsindex",
    ),
    path(
        _("doctors/assessments"),
        doctors.AssessmentListView.as_view(filter="active"),
        name="activeassessments",
    ),
    path(
        _("doctors/assessments/completed"),
        doctors.AssessmentListView.as_view(filter="completed"),
        name="completedassessments",
    ),
    path(
        _("doctors/assessments/my"),
        doctors.AssessmentListView.as_view(filter="my"),
        name="myassessments",
    ),
    path(
        _("doctors/assessments/my/active"),
        doctors.AssessmentListView.as_view(filter="myactive"),
        name="myactiveassessments",
    ),
    path(
        _("doctors/assessments/unclaimed"),
        doctors.AssessmentListView.as_view(filter="unclaimed"),
        name="unclaimedassessments",
    ),
    path("doctors/updatescores", doctors.updatescores, name="updatescores"),
    path(_("intro"), public.intro, name="intro"),
    path(_("login"), doctors.login, name="login"),
    path(_("logout"), doctors.logout, name="logout"),
    path(
        _("patientinfo"),
        public.PatientInformationView.as_view(),
        name="patientinfo",
    ),
    path(
        _("patientfactors"),
        public.PatientFactorsView.as_view(),
        name="patientfactors",
    ),
    path(_("result"), public.result, name="result"),
]
