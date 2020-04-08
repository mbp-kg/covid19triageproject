# -*- coding: UTF-8 -*-
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("covid19triage", "0005_assessments"),
    ]

    operations = [
        migrations.AddField(
            model_name="assessment",
            name="score",
            field=models.IntegerField(default=-1, verbose_name="Score"),
        ),
    ]
