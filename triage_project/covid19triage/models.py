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


class PatientFactors(models.Model):
    """
    Patient symptoms and risk factors
    """

    class Cough(models.TextChoices):
        NONE = "none", _("No cough")
        LIGHT = "light", _("Light cough")
        HEAVY = "heavy", _("Heavy cough")

    patient = models.ForeignKey(
        Patient,
        verbose_name=_("Patient"),
        on_delete=models.PROTECT,
    )
    symptoms = models.ManyToManyField("Symptom")
    cough = models.CharField(
        max_length=20,
        verbose_name=_("Description of cough"),
        choices=Cough.choices,
    )
    contact = models.BooleanField(
        verbose_name=_("Contact with a sick person"),
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
        unique=True,
        choices=Possible.choices
    )

    def __str__(self):
        return self.name
