from django import forms
from django.utils.translation import gettext, gettext_lazy as _
from django.utils.translation import pgettext, pgettext_lazy

from .models import ContactPerson

class ContactInformationForm(forms.ModelForm):
    """
    Contact Information
    """
    placeholder_firstname = pgettext_lazy("placeholder for first name", "John")
    firstname = forms.CharField(
        label=_("First Name"),
        help_text=_("Please enter your first or given name."),
        widget=forms.TextInput(
            attrs={"placeholder": placeholder_firstname},
        ),
    )
    placeholder_lastname = pgettext_lazy("placeholder for last name", "Doe")
    lastname = forms.CharField(
        label=_("Last Name"),
        help_text=_("Please enter your last or family name."),
        widget=forms.TextInput(
            attrs={"placeholder": placeholder_lastname},
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
