# -*- coding: UTF-8 -*-
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("covid19triage", "0006_assessment_score"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProposedDateTime",
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
                ("date", models.DateField()),
                ("time", models.TimeField()),
                ("ctime", models.DateTimeField(auto_now_add=True)),
                ("mtime", models.DateTimeField(auto_now=True)),
                (
                    "assessment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="covid19triage.Assessment",
                    ),
                ),
            ],
        ),
    ]
