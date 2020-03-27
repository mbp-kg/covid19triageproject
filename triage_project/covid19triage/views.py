from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.edit import FormView

from .forms import ContactInformationForm


def index(request):
    return render(request, "covid19triage/index.html", {})


class ContactInformationView(FormView):
    """
    Display the contact information form
    """
    form_class = ContactInformationForm
    template_name = "covid19triage/contactinfo.html"
