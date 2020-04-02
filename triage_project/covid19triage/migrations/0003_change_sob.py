# -*- coding: UTF-8 -*-
from django.db import migrations, models


def add_patientfactorversion(apps, schemaeditor):
    "Add new PatientFactors version"
    PFVModel = apps.get_model("covid19triage", "PatientFactorsVersion")

    version2 = PFVModel()
    version2.version = 2
    version2.description = (
        'Shortness of breath answer "moderate" becomes "mild"'
    )
    version2.save()


class Migration(migrations.Migration):

    dependencies = [("covid19triage", "0002_preload")]

    operations = [
        migrations.RunPython(add_patientfactorversion),
    ]
