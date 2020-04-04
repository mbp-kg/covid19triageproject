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
from .views import doctors
from .views import public

urlpatterns = [
    path("", public.index, name="index"),
    path(
        "contactinfo",
        public.ContactInformationView.as_view(),
        name="contactinfo",
    ),
    path(
        "doctors",
        doctors.PatientAssessmentsView.as_view(),
        name="doctorsindex",
    ),
    path("intro", public.intro, name="intro"),
    path("login", doctors.login, name="login"),
    path("logout", doctors.logout, name="logout"),
    path(
        "patientinfo",
        public.PatientInformationView.as_view(),
        name="patientinfo",
    ),
    path(
        "patientfactors",
        public.PatientFactorsView.as_view(),
        name="patientfactors",
    ),
    path("result", public.result, name="result"),
]
