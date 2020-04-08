import datetime
import decimal

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext, gettext_lazy as _


class Assessment(models.Model):
    """
    A patientʼs assessment
    """

    # Status states
    # 1. New assessments begin in the UNCLAIMED state.
    # 2. If the assessment is a test of the software, the state will be changed
    #    to TESTING.  If the assessment is reviewed by a doctor and no further
    #    action is required, the state will be changed to NOFURTHERACTION.  If
    #    the assessment requires contact with the patient, a doctor may claim
    #    the assessment and attempt to contact the patient by changing the
    #    state to CLAIMED.
    # 3. If the doctor contacts the patient and refers the patient for
    #    treatment, the doctor should change the state to REFERREDFORTREATMENT.
    #    If the patient needs no further care, the doctor should change the
    #    state to NOFURTHERACTION.  If the doctor is unable to make contact
    #    with the patient, the doctor should change the state of
    #    AWAITINGCONTACT.  Finally, if a doctor is unable to handle an
    #    assessment, the doctor should return the state to UNCLAIMED.
    class Status(models.TextChoices):
        TESTING = "testing", _("Complete – testing")
        NOFURTHERACTION = (
            "no further action",
            _("Complete – No further action"),
        )
        REFERREDFORTREATMENT = (
            "referred for treatment",
            _("Complete – Patient referred for treatment"),
        )
        AWAITINGPATIENT = (
            "awaiting patient",
            _("Active – Awaiting patient contact"),
        )
        CLAIMED = "claimed", _("Active – Claimed")
        UNCLAIMED = "unclaimed", _("Active – Unclaimed")

    status = models.CharField(
        max_length=30,
        verbose_name=_("Status"),
        help_text=_("Status of the assessment"),
        choices=Status.choices,
        default=Status.UNCLAIMED,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True,
    )
    patientfactors = models.ForeignKey(
        "PatientFactors", on_delete=models.PROTECT,
    )
    ctime = models.DateTimeField(auto_now_add=True,)
    mtime = models.DateTimeField(auto_now=True,)
    version = models.IntegerField(
        verbose_name=_("Version"),
        help_text=_("Version is incremented with each change."),
        default=0,
    )
    score = models.IntegerField(verbose_name=_("Score"), default=-1,)

    def updated(self) -> datetime.datetime:
        lastassessmentlog = (
            AssessmentLog.objects.filter(assessment=self)
            .order_by("-mtime")
            .first()
        )
        if lastassessmentlog is not None:
            return max(lastassessmentlog.mtime, self.mtime)
        else:
            return self.mtime

    def __str__(self):
        return "{}: {}, {}".format(self.patientfactors.patient, self.score, self.status)


class AssessmentLog(models.Model):
    """
    A log of actions taken regarding an assessment

    These actions might include changing the status of the assessment
    A doctor's opinion of a PatientFactors (symptoms and risk factors)
    """

    assessment = models.ForeignKey(Assessment, on_delete=models.PROTECT,)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
    )
    comments = models.TextField(verbose_name=_("Comments"),)
    ctime = models.DateTimeField(auto_now_add=True,)
    mtime = models.DateTimeField(auto_now=True,)


class ContactPerson(models.Model):
    """
    A person with contact information
    """

    class ForWhom(models.TextChoices):
        SELF = "self", _("For myself")
        OTHER = "other", _("For someone else")

    firstname = models.CharField(max_length=200, verbose_name=_("First name"),)
    lastname = models.CharField(max_length=200, verbose_name=_("Last name"),)
    phonenumber = models.CharField(
        max_length=30, verbose_name=_("Phone number"),
    )
    emailaddress = models.CharField(
        max_length=200, verbose_name=_("Email address"), blank=True,
    )
    forwhom = models.CharField(
        max_length=5,
        verbose_name=_("Who is the patient?"),
        help_text=_("Is the contact person answering for herself or himself?"),
        choices=ForWhom.choices,
    )
    ctime = models.DateTimeField(auto_now_add=True,)
    mtime = models.DateTimeField(auto_now=True,)

    def __str__(self):
        return "{}, {}".format(self.lastname, self.firstname)


class Patient(models.Model):
    """
    A potential patient
    """

    class MedicalGender(models.TextChoices):
        FEMALE = "f", _("Female")
        MALE = "m", _("Male")

    contactperson = models.ForeignKey(
        ContactPerson,
        verbose_name=_("Contact Person"),
        on_delete=models.PROTECT,
    )
    firstname = models.CharField(max_length=200, verbose_name=_("First name"),)
    lastname = models.CharField(max_length=200, verbose_name=_("Last name"),)
    gender = models.CharField(
        max_length=1, verbose_name=_("Gender"), choices=MedicalGender.choices,
    )
    dob = models.DateField(verbose_name=_("Date of Birth"),)
    ctime = models.DateTimeField(auto_now_add=True,)
    mtime = models.DateTimeField(auto_now=True,)

    def __str__(self):
        return ", ".join([self.lastname, self.firstname])

    def ageindays(self, todaytz=None):
        if todaytz is None:
            todaytz = timezone.now().date()
        return (todaytz - self.dob).days


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

    class ShortnessOfBreathV2(models.TextChoices):
        NONE = "none", _("No shortness of breath")
        MILD = "mild", _("Mild shortness of breath")
        SEVERE = "severe", _("Severe shortness of breath")

    patient = models.ForeignKey(
        Patient, verbose_name=_("Patient"), on_delete=models.PROTECT,
    )
    symptoms = models.ManyToManyField("Symptom", blank=True,)
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
        choices=ShortnessOfBreathV2.choices,
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
    risks = models.ManyToManyField("Risk", blank=True,)
    cancer = models.BooleanField(
        verbose_name=_("The patient is being treated for cancer"),
    )
    ctime = models.DateTimeField(auto_now_add=True,)
    mtime = models.DateTimeField(auto_now=True,)
    version = models.ForeignKey(
        "PatientFactorsVersion",
        verbose_name=_("Version"),
        on_delete=models.PROTECT,
    )

    def __str__(self):
        items = []
        symptoms = ", ".join([str(s) for s in self.symptoms.all()])
        if symptoms:
            items.append(symptoms)
        temp = (
            str(self.normalized_temperature()) if self.temperature else ""
        )
        if temp:
            items.append(temp)
        cough = (
            "cough: " + self.cough
            if self.cough != PatientFactors.Cough.NONE
            else ""
        )
        if cough:
            items.append(cough)
        sob = (
            "shortness of breath: " + self.shortnessofbreath
            if self.shortnessofbreath
            != PatientFactors.ShortnessOfBreath.NONE
            and self.shortnessofbreath
            != PatientFactors.ShortnessOfBreathV2.NONE
            else ""
        )
        if sob:
            items.append(sob)
        if self.pregnant:
            items.append("pregnant or expecting to become")
        if self.contact:
            items.append("contact with sick")
        if self.smokeorvape:
            items.append("smoker")
        risks = ", ".join([str(s) for s in self.risks.all()])
        if risks:
            items.append(risks)
        if self.cancer:
            items.append("being treated for cancer")
        return "{}: {}".format(str(self.patient), ", ".join(items),)

    def normalized_temperature(self):
        c = decimal.getcontext()
        # Decrease decimal precision
        c.prec = 4
        if self.temperature > decimal.Decimal(80, c):
            ratio = decimal.Decimal(5, c) / decimal.Decimal(9, c)
            tempc = (self.temperature - decimal.Decimal(32, c)) * ratio
            return tempc
        return self.temperature

    class Meta:
        verbose_name_plural = _("PatientFactors")


class PatientFactorsVersion(models.Model):
    """
    Versions of the Patient Factors questions
    """

    version = models.IntegerField(
        unique=True, verbose_name=_("Version of the PatientFactors questions"),
    )
    description = models.TextField(
        verbose_name=_("Description of the changes in this version"),
    )


class Risk(models.Model):
    """
    Risks for of patients possibly experiencing COVID-19
    """

    class Possible(models.TextChoices):
        RESPIRATORY = (
            "respiratory",
            _("Respiratory condition, e.g., COPD, asthma"),
        )
        HEART = "heart", _("Heart condition")
        DIABETES = "diabetes", _("Diabetes")
        CHRONIC_CONDITION = (
            "chronic condition",
            _("Other chronic condition, e.g., kidney failure, liver failure"),
        )
        IMMUNOCOMPROMISED = "immunocompromised", _("Immunocompromised")

    name = models.CharField(
        max_length=30, primary_key=True, choices=Possible.choices
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

    name = models.CharField(
        max_length=20, primary_key=True, choices=Possible.choices
    )

    def __str__(self):
        return self.name


def get_current_pfv():
    return PatientFactorsVersion.objects.get(pk=2)
