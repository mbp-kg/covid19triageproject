from django import forms
from django.utils.translation import gettext, gettext_lazy as _
from django.utils.translation import pgettext, pgettext_lazy as _p

from .models import ContactPerson

class ContactInformationForm(forms.ModelForm):
    """
    Contact Information
    """
    firstname = forms.CharField(
        label=_("First Name"),
        help_text=_("Please enter your first or given name."),
        widget=forms.TextInput(
            attrs={"placeholder": _p("placeholder for first name", "John")},
        ),
    )
    lastname = forms.CharField(
        label=_("Last Name"),
        help_text=_("Please enter your last or family name."),
        widget=forms.TextInput(
            attrs={"placeholder": _p("placeholder for last name", "Doe")},
        ),
    )
    phonenumber = forms.CharField(
        label=_("Phone Number"),
        help_text=_("Please enter a phone number where we can reach you."),
        widget=forms.TextInput(
            attrs={"placeholder": "0 (555) 555-555"},
        ),
    )
    emailaddress = forms.CharField(
        label=_("E-mail address"),
        help_text=_("Please enter your e-mail address."),
        widget=forms.TextInput(
            attrs={"placeholder": "example@example.com"},
        ),
    )

    class Meta:
        model = ContactPerson
        exclude = []
