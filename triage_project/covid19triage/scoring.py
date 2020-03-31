from django.utils import timezone

from .models import Patient
from .models import PatientFactors
from .models import Risk
from .models import Symptom


def calculate_score(patient: Patient, patientfactors: PatientFactors) -> int:

    weight = {
        "age": 3,
        "smoking": 1,
        "fever38": 3,
        "fever39": 5,
        "cough": 3,
        "shortnessofbreathmoderate": 2,
        "shortnessofbreathsevere": 5,
        "chroniclung": 5,
        "chronicheart": 3,
        "chronicother": 3,
        "cancertreatment": 5,
        "immunodeficient": 3,
        "contact": 2,
    }
    scores = {
        "age": 0,
        "smoking": 0,
        "fever38": 0,
        "fever39": 0,
        "cough": 0,
        "shortnessofbreath": 0,
        "chroniclung": 0,
        "chronicheart": 0,
        "chronicother": 0,
        "cancertreatment": 0,
        "immunodeficient": 0,
        "contact": 0,
    }

    today = timezone.now().date()
    agetwo = 365.25 * 2
    agesixtyfive = 365.25 * 65
    age = (today - patient.dob).days
    if age < agetwo or age > agesixtyfive:
        scores["age"] += weight["age"]

    if patientfactors.smokeorvape:
        scores["smoking"] += weight["smoking"]

    # FIXME: Convert F to C
    if patientfactors.temperature > 39.0:
        scores["fever39"] += weight["fever39"]
    elif patientfactors.temperature > 38.0:
        scores["fever38"] += weight["fever38"]

    if patientfactors.cough in [
        PatientFactors.Cough.WET,
        PatientFactors.Cough.DRY,
    ]:
        scores["cough"] += weight["cough"]

    if patientfactors.symptoms.filter(
        pk=Symptom.Possible.SHORTNESS_OF_BREATH
    ).exists():
        if (
            patientfactors.shortnessofbreath
            == PatientFactors.ShortnessOfBreath.MODERATE
        ):
            scores["shortnessofbreath"] += weight["shortnessofbreathmoderate"]
        elif (
            patientfactors.shortnessofbreath
            == PatientFactors.ShortnessOfBreath.SEVERE
        ):
            scores["shortnessofbreath"] += weight["shortnessofbreathsevere"]

    if patientfactors.risks.filter(pk=Risk.Possible.RESPIRATORY).exists():
        scores["chroniclung"] += weight["chroniclung"]

    if patientfactors.risks.filter(pk=Risk.Possible.HEART).exists():
        scores["chronicheart"] += weight["chronicheart"]

    if (
        patientfactors.risks.filter(pk=Risk.Possible.DIABETES).exists()
        or patientfactors.symptoms.filter(
            pk=Risk.Possible.CHRONIC_CONDITION
        ).exists()
    ):
        scores["chronicother"] += weight["chronicother"]

    if patientfactors.risks.filter(
        pk=Risk.Possible.IMMUNOCOMPROMISED
    ).exists():
        scores["immunodeficient"] += weight["immunodeficient"]

    if patientfactors.cancer:
        scores["cancertreatment"] += weight["cancertreatment"]

    if patientfactors.contact:
        scores["contact"] += weight["contact"]

    return sum(scores.values())
