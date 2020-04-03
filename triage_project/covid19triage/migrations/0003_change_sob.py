# -*- coding: UTF-8 -*-
from django.db import migrations
from django.db import models


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
        migrations.AlterField(
            model_name="patientfactors",
            name="shortnessofbreath",
            field=models.CharField(
                choices=[
                    ("none", "No shortness of breath"),
                    ("mild", "Mild shortness of breath"),
                    ("severe", "Severe shortness of breath"),
                ],
                max_length=20,
                verbose_name="Description of shortness of breath",
            ),
        ),
    ]
