from django.db import models
from django.utils.translation import gettext, gettext_lazy as _


class ContactPerson(models.Model):
    """
    A person with contact information
    """
    firstname = models.CharField(
        max_length=200,
        verbose_name=_("First name"),
    )
    lastname = models.CharField(
        max_length=200,
        verbose_name=_("Last name"),
    )
    phonenumber = models.CharField(
        max_length=30,
        verbose_name=_("Phone number"),
    )
    emailaddress = models.CharField(
        max_length=200,
        verbose_name=_("Email address"),
        blank=True,
    )
    ctime = models.DateTimeField(
        auto_now_add=True,
    )
    mtime = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return "{}, {}".format(self.lastname, self.firstname)


class Patient(models.Model):
    """
    A potential patient
    """

    class ForWhom(models.TextChoices):
        SELF = "self", _("For myself")
        OTHER = "other", _("For someone else")

    class MedicalGender(models.TextChoices):
        FEMALE = "f", _("Female")
        MALE = "m", _("Male")

    forwhom = models.CharField(
        max_length=5,
        verbose_name=_("Who is the patient?"),
        help_text=_("Is the contact person answering for herself or himself?"),
        choices=ForWhom.choices,
    )
    firstname = models.CharField(
        max_length=200,
        verbose_name=_("First name"),
    )
    lastname = models.CharField(
        max_length=200,
        verbose_name=_("Last name"),
    )
    gender = models.CharField(
        max_length=1,
        verbose_name=_("Gender"),
        choices=MedicalGender.choices,
    )
    dob = models.DateField(
        verbose_name=_("Date of Birth"),
    )
    ctime = models.DateTimeField(
        auto_now_add=True,
    )
    mtime = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return "{}, {}".format(self.lastname, self.firstname)


class PatientFactors(models.Model):
    """
    Patient symptoms and risk factors
    """

    class Cough(models.TextChoices):
        NONE = "none", _("No cough")
        WET = "wet", _("Wet cough")
        DRY = "dry", _("Dry cough")

    class ShortnessOfBreath(models.TextChoices):
        NONE = "none", _("No shortness of breath")
        MODERATE = "moderate", _("Moderate shortness of breath")
        SEVERE = "severe", _("Severe shortness of breath")

    patient = models.ForeignKey(
        Patient,
        verbose_name=_("Patient"),
        on_delete=models.PROTECT,
    )
    symptoms = models.ManyToManyField("Symptom")
    temperature = models.DecimalField(
        decimal_places=1,
        max_digits=4,
        verbose_name=_("Patientʼs highest temperature within 24 hours"),
        null=True,
    )
    cough = models.CharField(
        max_length=20,
        verbose_name=_("Description of cough"),
        choices=Cough.choices,
    )
    shortnessofbreath = models.CharField(
        max_length=20,
        verbose_name=_("Description of shortness of breath"),
        choices=ShortnessOfBreath.choices,
    )
    pregnant = models.BooleanField(
        verbose_name=_("Patient is pregnant or expecting to become pregnant")
    )
    contact = models.BooleanField(
        verbose_name=_("Contact with a sick person"),
    )
    smokeorvape = models.BooleanField(
        verbose_name=_("The patient smokes or vapes"),
    )
    risks = models.ManyToManyField("Risk")
    cancer = models.BooleanField(
        verbose_name=_("The patient is being treated for cancer"),
    )
    ctime = models.DateTimeField(
        auto_now_add=True,
    )
    mtime = models.DateTimeField(
        auto_now=True,
    )
    version = models.ForeignKey(
        "PatientFactorsVersion",
        verbose_name=_("Version"),
        on_delete=models.PROTECT,
    )

    class Meta:
        verbose_name_plural = _("PatientFactors")


class PatientFactorsVersion(models.Model):
    """
    Versions of the Patient Factors questions
    """
    version = models.IntegerField(
        unique=True,
        verbose_name=_("Version of the PatientFactors questions"),
    )
    description = models.TextField(
        verbose_name=_("Description of the changes in this version"),
    )


class Risk(models.Model):
    """
    Risks for of patients possibly experiencing COVID-19
    """

    class Possible(models.TextChoices):
        RESPIRATORY = "respiratory", _("Respiratory condition, e.g., COPD, asthma")
        HEART = "heart", _("Heart condition")
        DIABETES = "diabetes", _("Diabetes")
        CHRONIC_CONDITION = "chronic condition", _("Other chronic condition, e.g., kidney failure, liver failure")
        IMMUNOCOMPROMISED = "immunocompromised", _("Immunocompromised")
        NONE = "none", _("None of these")

    name = models.CharField(
        max_length=30,
        primary_key=True,
        choices=Possible.choices
    )

    def __str__(self):
        return self.name


class Symptom(models.Model):
    """
    Symptoms of COVID-19
    """

    class Possible(models.TextChoices):
        FEVER = "fever", _("Temperature at or above 38°C (100.4°F)")
        COUGH = "cough", _("Cough")
        SHORTNESS_OF_BREATH = "shortness of breath", _("Shortness of breath")
        NONE = "none", _("None of these")

    name = models.CharField(
        max_length=20,
        primary_key=True,
        choices=Possible.choices
    )

    def __str__(self):
        return self.name


def get_current_pfv():
    return PatientFactorsVersion.objects.get(pk=1)
