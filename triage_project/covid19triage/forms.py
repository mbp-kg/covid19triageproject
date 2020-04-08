# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import gettext, gettext_lazy as _
from django.utils.translation import pgettext, pgettext_lazy

from .fields import StrictBooleanField
from .models import Assessment
from .models import ContactPerson
from .models import Patient
from .models import PatientFactors
from .models import Risk
from .models import Symptom
from .widgets import KnownNullBooleanSelect


class AssessmentForm(forms.ModelForm):
    """
    A doctor's assessment
    """

    status = forms.ChoiceField(
        choices=Assessment.Status.choices,
        label=_("Status"),
        help_text=_("Optionally change the status of this assessment"),
    )
    version = forms.IntegerField(widget=forms.HiddenInput(),)

    class Meta:
        fields = (
            "status",
            "version",
        )
        model = Assessment


class ContactInformationForm(forms.ModelForm):
    """
    Contact Information
    """

    placeholder_firstname = pgettext_lazy("placeholder for first name", "John")
    firstname = forms.CharField(
        label=_("First Name"),
        help_text=_("Please enter your first or given name."),
        widget=forms.TextInput(attrs={"placeholder": placeholder_firstname},),
    )
    placeholder_lastname = pgettext_lazy("placeholder for last name", "Doe")
    lastname = forms.CharField(
        label=_("Last Name"),
        help_text=_("Please enter your last or family name."),
        widget=forms.TextInput(attrs={"placeholder": placeholder_lastname},),
    )
    phonenumber = forms.CharField(
        label=_("Phone Number"),
        help_text=_("Please enter a phone number where we can reach you."),
        widget=forms.TextInput(attrs={"placeholder": "0 (555) 555-555"},),
    )
    emailaddress = forms.CharField(
        label=_("E-mail address"),
        help_text=_("Please enter your e-mail address."),
        widget=forms.TextInput(attrs={"placeholder": "example@example.com"},),
    )
    forwhom = forms.ChoiceField(
        label=_("Are you answering for yourself?"),
        help_text=_("Who is the patient?"),
        choices=ContactPerson.ForWhom.choices,
    )

    class Meta:
        model = ContactPerson
        fields = [
            "firstname",
            "lastname",
            "phonenumber",
            "emailaddress",
            "forwhom",
        ]


class PatientFactorsForm(forms.ModelForm):
    """
    Patient symptoms and risk factors
    """

    symptoms = forms.MultipleChoiceField(
        choices=Symptom.Possible.choices,
        widget=forms.CheckboxSelectMultiple(),
        label=_("Does the patient have any of the following symptoms?"),
        required=False,
    )
    temperature = forms.DecimalField(
        decimal_places=1,
        max_digits=4,
        max_value=110.0,
        min_value=30.0,
        label=_("Patientʼs highest temperature within 24 hours"),
        required=False,
    )
    cough = forms.ChoiceField(
        label=_("How would the patient describe the patientʼs cough?"),
        help_text=_("Is it intense?"),
        choices=PatientFactors.Cough.choices,
    )
    shortnessofbreath = forms.ChoiceField(
        label=_(
            "How would the patient describe the patientʼs shortness of breath?"
        ),
        help_text=_("Is it severe?"),
        choices=PatientFactors.ShortnessOfBreathV2.choices,
    )
    pregnant = forms.BooleanField(
        label=_("Is the patient pregnant or expecting to become pregnant?"),
        required=False,
    )
    contact = StrictBooleanField(
        label=_("Has the patient been in contact with someone who is sick?"),
        widget=KnownNullBooleanSelect(),
    )
    smokeorvape = forms.BooleanField(
        label=_("Does the patient smoke or vape or use e-cigarettes?"),
        required=False,
    )
    risks = forms.MultipleChoiceField(
        choices=Risk.Possible.choices,
        widget=forms.CheckboxSelectMultiple(),
        label=_("Does the patient have any of the following conditions?"),
        required=False,
    )
    cancer = forms.BooleanField(
        label=_("Is the patient currently under treatment for cancer?"),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically require temperature
        if "data" in kwargs and kwargs["data"]:
            symptoms = kwargs["data"].get("symptoms")
            if symptoms is not None and Symptom.Possible.FEVER in symptoms:
                self.fields["temperature"].required = True

    class Meta:
        model = PatientFactors
        fields = [
            "symptoms",
            "temperature",
            "cough",
            "shortnessofbreath",
            "pregnant",
            "contact",
            "smokeorvape",
            "risks",
            "cancer",
        ]


class PatientInformationForm(forms.ModelForm):
    """
    Patient Information
    """

    placeholder_firstname = pgettext_lazy("placeholder for first name", "John")
    firstname = forms.CharField(
        label=_("Patientʼs First Name"),
        help_text=_("Please enter the patientʼs first or given name."),
        widget=forms.TextInput(attrs={"placeholder": placeholder_firstname},),
    )
    placeholder_lastname = pgettext_lazy("placeholder for last name", "Doe")
    lastname = forms.CharField(
        label=_("Patientʼs Last Name"),
        help_text=_("Please enter the patientʼs last or family name."),
        widget=forms.TextInput(attrs={"placeholder": placeholder_lastname},),
    )
    gender = forms.ChoiceField(
        label=_("Patientʼs Gender"),
        help_text=_("Please enter the patientʼs medical gender."),
        choices=Patient.MedicalGender.choices,
    )
    dob = forms.DateField(
        label=_("Patientʼs Date of Birth"),
        help_text=_("Please enter the patientʼs date of birth."),
        widget=forms.DateInput(attrs={"type": "date"},),
    )

    class Meta:
        model = Patient
        fields = [
            "firstname",
            "lastname",
            "gender",
            "dob",
        ]
