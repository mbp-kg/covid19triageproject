# -*- coding: UTF-8 -*-
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ContactPerson",
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
                    "firstname",
                    models.CharField(
                        max_length=200, verbose_name="First name"
                    ),
                ),
                (
                    "lastname",
                    models.CharField(max_length=200, verbose_name="Last name"),
                ),
                (
                    "phonenumber",
                    models.CharField(
                        max_length=30, verbose_name="Phone number"
                    ),
                ),
                (
                    "emailaddress",
                    models.CharField(
                        blank=True,
                        max_length=200,
                        verbose_name="Email address",
                    ),
                ),
                (
                    "forwhom",
                    models.CharField(
                        choices=[
                            ("self", "For myself"),
                            ("other", "For someone else"),
                        ],
                        help_text="Is the contact person answering for herself or himself?",
                        max_length=5,
                        verbose_name="Who is the patient?",
                    ),
                ),
                ("ctime", models.DateTimeField(auto_now_add=True)),
                ("mtime", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Patient",
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
                    "firstname",
                    models.CharField(
                        max_length=200, verbose_name="First name"
                    ),
                ),
                (
                    "lastname",
                    models.CharField(max_length=200, verbose_name="Last name"),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[("f", "Female"), ("m", "Male")],
                        max_length=1,
                        verbose_name="Gender",
                    ),
                ),
                ("dob", models.DateField(verbose_name="Date of Birth")),
                ("ctime", models.DateTimeField(auto_now_add=True)),
                ("mtime", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="PatientFactorsVersion",
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
                    "version",
                    models.IntegerField(
                        unique=True,
                        verbose_name="Version of the PatientFactors questions",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        verbose_name="Description of the changes in this version"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Risk",
            fields=[
                (
                    "name",
                    models.CharField(
                        choices=[
                            (
                                "respiratory",
                                "Respiratory condition, e.g., COPD, asthma",
                            ),
                            ("heart", "Heart condition"),
                            ("diabetes", "Diabetes"),
                            (
                                "chronic condition",
                                "Other chronic condition, e.g., kidney failure, liver failure",
                            ),
                            ("immunocompromised", "Immunocompromised"),
                        ],
                        max_length=30,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Symptom",
            fields=[
                (
                    "name",
                    models.CharField(
                        choices=[
                            (
                                "fever",
                                "Temperature at or above 38°C (100.4°F)",
                            ),
                            ("cough", "Cough"),
                            ("shortness of breath", "Shortness of breath"),
                        ],
                        max_length=20,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PatientFactors",
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
                    "temperature",
                    models.DecimalField(
                        decimal_places=1,
                        max_digits=4,
                        null=True,
                        verbose_name="Patientʼs highest temperature within 24 hours",
                    ),
                ),
                (
                    "cough",
                    models.CharField(
                        choices=[
                            ("none", "No cough"),
                            ("wet", "Wet cough"),
                            ("dry", "Dry cough"),
                        ],
                        max_length=20,
                        verbose_name="Description of cough",
                    ),
                ),
                (
                    "shortnessofbreath",
                    models.CharField(
                        choices=[
                            ("none", "No shortness of breath"),
                            ("moderate", "Moderate shortness of breath"),
                            ("severe", "Severe shortness of breath"),
                        ],
                        max_length=20,
                        verbose_name="Description of shortness of breath",
                    ),
                ),
                (
                    "pregnant",
                    models.BooleanField(
                        verbose_name="Patient is pregnant or expecting to become pregnant"
                    ),
                ),
                (
                    "contact",
                    models.BooleanField(
                        verbose_name="Contact with a sick person"
                    ),
                ),
                (
                    "smokeorvape",
                    models.BooleanField(
                        verbose_name="The patient smokes or vapes"
                    ),
                ),
                (
                    "cancer",
                    models.BooleanField(
                        verbose_name="The patient is being treated for cancer"
                    ),
                ),
                ("ctime", models.DateTimeField(auto_now_add=True)),
                ("mtime", models.DateTimeField(auto_now=True)),
                (
                    "patient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="covid19triage.Patient",
                        verbose_name="Patient",
                    ),
                ),
                (
                    "risks",
                    models.ManyToManyField(
                        blank=True, to="covid19triage.Risk"
                    ),
                ),
                (
                    "symptoms",
                    models.ManyToManyField(
                        blank=True, to="covid19triage.Symptom"
                    ),
                ),
                (
                    "version",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="covid19triage.PatientFactorsVersion",
                        verbose_name="Version",
                    ),
                ),
            ],
            options={"verbose_name_plural": "PatientFactors",},
        ),
    ]
