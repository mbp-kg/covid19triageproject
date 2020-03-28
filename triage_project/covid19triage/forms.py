from django import forms
from django.utils.translation import gettext, gettext_lazy as _
from django.utils.translation import pgettext, pgettext_lazy

from .models import ContactPerson
from .models import Patient
from .models import PatientFactors
from .models import Symptom

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
        fields = "__all__"


class PatientFactorsForm(forms.ModelForm):
    """
    Patient symptoms and risk factors
    """
    symptoms = forms.MultipleChoiceField(
        choices=Symptom.Possible.choices,
        widget=forms.CheckboxSelectMultiple(),
        label=_("Symptoms"),
        help_text=_("Do you have any of the following symptoms?"),
    )
    cough = forms.ChoiceField(
        label=_("How would you describe your cough?"),
        help_text=_("Is it intense?"),
        choices=PatientFactors.Cough.choices,
    )

    class Meta:
        model = PatientFactors
        fields = ["symptoms", "cough", "contact"]


class PatientInformationForm(forms.ModelForm):
    """
    Patient Information
    """
    forwhom = forms.ChoiceField(
        label=_("Are you answering for yourself?"),
        help_text=_("Who is the patient?"),
        choices=Patient.ForWhom.choices,
    )
    placeholder_firstname = pgettext_lazy("placeholder for first name", "John")
    firstname = forms.CharField(
        label=_("First Name"),
        help_text=_("Please enter the patientʼs first or given name."),
        widget=forms.TextInput(
            attrs={"placeholder": placeholder_firstname},
        ),
    )
    placeholder_lastname = pgettext_lazy("placeholder for last name", "Doe")
    lastname = forms.CharField(
        label=_("Last Name"),
        help_text=_("Please enter the patientʼs last or family name."),
        widget=forms.TextInput(
            attrs={"placeholder": placeholder_lastname},
        ),
    )
    gender = forms.ChoiceField(
        label=("Gender"),
        help_text=_("Please enter the patientʼs medical gender."),
        choices=Patient.MedicalGender.choices,
    )

    class Meta:
        model = Patient
        fields = "__all__"
