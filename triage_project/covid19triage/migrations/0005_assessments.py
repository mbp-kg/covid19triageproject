# -*- coding: UTF-8 -*-
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def create_assessments_for_patientfactors(apps, schemaeditor):
    "Create an Assessment for each PatientFactors"
    AssessmentModel = apps.get_model("covid19triage", "Assessment")
    PatientFactorsModel = apps.get_model("covid19triage", "PatientFactors")

    for pf in PatientFactorsModel.objects.all():
        assessment = AssessmentModel()
        assessment.owner = None
        assessment.patientfactors = pf
        assessment.version = 1
        assessment.save()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("covid19triage", "0004_contactperson_for_patient"),
    ]

    operations = [
        migrations.CreateModel(
            name="Assessment",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("testing", "Complete – testing"),
                            (
                                "no further action",
                                "Complete – No further action",
                            ),
                            (
                                "referred for treatment",
                                "Complete – Patient referred for treatment",
                            ),
                            (
                                "awaiting patient",
                                "Active – Awaiting patient contact",
                            ),
                            ("claimed", "Active – Claimed"),
                            ("unclaimed", "Active – Unclaimed"),
                        ],
                        default="unclaimed",
                        help_text="Status of the assessment",
                        max_length=30,
                        verbose_name="Status",
                    ),
                ),
                ("ctime", models.DateTimeField(auto_now_add=True)),
                ("mtime", models.DateTimeField(auto_now=True)),
                (
                    "version",
                    models.IntegerField(
                        default=0,
                        help_text="Version is incremented with each change.",
                        verbose_name="Version",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "patientfactors",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="covid19triage.PatientFactors",
                    ),
                ),
            ],
        ),
        # I do not understand why Django (manage.py makemigrations) thinks that
        # this AlterField is necessary.  It seems that the on_delete=PROTECT
        # setting is already present in
        # migrations/0004_contactperson_for_patient.py.
        migrations.AlterField(
            model_name="patient",
            name="contactperson",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="covid19triage.ContactPerson",
                verbose_name="Contact Person",
            ),
        ),
        migrations.CreateModel(
            name="AssessmentLog",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("comments", models.TextField(verbose_name="Comments")),
                ("ctime", models.DateTimeField(auto_now_add=True)),
                ("mtime", models.DateTimeField(auto_now=True)),
                (
                    "assessment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="covid19triage.Assessment",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.RunPython(create_assessments_for_patientfactors),
    ]
