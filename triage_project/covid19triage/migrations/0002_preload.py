# -*- coding: UTF-8 -*-
from django.db import migrations, models


def add_patientfactorversion(apps, schemaeditor):
    "Add initial PatientFactors version"
    PFVModel = apps.get_model("covid19triage", "PatientFactorsVersion")

    version1 = PFVModel()
    version1.version = 1
    version1.description = "Initial version of the questions"
    version1.save()


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
        migrations.RunPython(add_symptoms),
    ]
