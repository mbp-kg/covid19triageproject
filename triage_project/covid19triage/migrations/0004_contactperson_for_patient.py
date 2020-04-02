# -*- coding: UTF-8 -*-
import logging

from django.db import migrations, models
import django.db.models.deletion


logger = logging.getLogger(__name__)


def update_patient_contactperson(apps, schemaeditor):
    "Add a contactperson to existing patients"
    ContactPersonModel = apps.get_model("covid19triage", "ContactPerson")
    PatientModel = apps.get_model("covid19triage", "Patient")

    for patient in PatientModel.objects.all():
        tenativeid = patient.pk
        try:
            contactperson = ContactPersonModel.objects.get(pk=tenativeid)
            patient.contactperson = contactperson
            patient.save()
        except ContactPersonModel.DoesNotExist:
            logger.warn(
                "Patient(pk={}) has no ContactPerson".format(patient.pk)
            )


class Migration(migrations.Migration):

    dependencies = [
        ("covid19triage", "0003_change_sob"),
    ]

    operations = [
        migrations.AddField(
            model_name="patient",
            name="contactperson",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                to="covid19triage.ContactPerson",
                verbose_name="ContactPerson",
            ),
            preserve_default=False,
        ),
        migrations.RunPython(update_patient_contactperson),
    ]
