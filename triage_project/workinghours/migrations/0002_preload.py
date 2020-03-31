# -*- coding: UTF-8 -*-
from django.db import migrations, models

from datetime import time


def add_timezone(apps, schemaeditor):
    "Add initial working hours"
    TimezoneModel = apps.get_model("workinghours", "Timezone")
    tz = TimezoneModel()
    tz.tz = "Asia/Bishkek"
    tz.save()


def add_workdays(apps, schemaeditor):
    "Add initial working hours"
    WorkDayModel = apps.get_model("workinghours", "WorkDay")

    workdays = [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
    ]
    for workday in workdays:
        model = WorkDayModel()
        model.dayofweek = workday
        model.openfrom = time(9)
        model.closedafter = time(17)
        model.save()

    saturday = WorkDayModel()
    saturday.dayofweek = "saturday"
    saturday.openfrom = time(9)
    saturday.closedafter = time(13)
    saturday.save()


class Migration(migrations.Migration):

    dependencies = [("workinghours", "0001_initial")]

    operations = [
        migrations.RunPython(add_timezone),
        migrations.RunPython(add_workdays),
    ]
