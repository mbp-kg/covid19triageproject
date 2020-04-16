# -*- coding: UTF-8 -*-
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("covid19triage", "0007_proposeddatetime"),
    ]

    operations = [
        migrations.AlterField(
            model_name="assessmentlog",
            name="assessment",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="logs",
                to="covid19triage.Assessment",
            ),
        ),
    ]
