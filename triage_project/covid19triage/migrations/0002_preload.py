# -*- coding: UTF-8 -*-
from django.db import migrations, models


def add_patientfactorversion(apps, schemaeditor):
    "Add initial PatientFactors version"
    PFVModel = apps.get_model("covid19triage", "PatientFactorsVersion")

    version1 = PFVModel()
    version1.version = 1
    version1.description = "Initial version of the questions"
    version1.save()


def add_risks(apps, schemaeditor):
    "Add patient risks"
    RiskModel = apps.get_model("covid19triage", "Risk")

    respiratory = RiskModel()
    respiratory.name = "respiratory"
    respiratory.save()

    heart = RiskModel()
    heart.name = "heart"
    heart.save()

    diabetes = RiskModel()
    diabetes.name = "diabetes"
    diabetes.save()

    chroniccondition = RiskModel()
    chroniccondition.name = "chronic condition"
    chroniccondition.save()

    immunocompromised = RiskModel()
    immunocompromised.name = "immunocompromised"
    immunocompromised.save()


def add_symptoms(apps, schemaeditor):
    "Add symptoms"
    SymptomModel = apps.get_model("covid19triage", "Symptom")

    fever = SymptomModel()
    fever.name = "fever"
    fever.save()

    cough = SymptomModel()
    cough.name = "cough"
    cough.save()

    shortnessofbreath = SymptomModel()
    shortnessofbreath.name = "shortness of breath"
    shortnessofbreath.save()


class Migration(migrations.Migration):

    dependencies = [("covid19triage", "0001_initial")]

    operations = [
        migrations.RunPython(add_patientfactorversion),
        migrations.RunPython(add_risks),
        migrations.RunPython(add_symptoms),
    ]
