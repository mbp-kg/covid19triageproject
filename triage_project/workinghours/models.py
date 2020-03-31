from django.db import models
from django.utils.translation import gettext_lazy as _


class Timezone(models.Model):
    """
    The timezone to use for working hours
    """

    tz = models.CharField(primary_key=True, max_length=200, verbose_name=_("Timezone"),)


class WorkDay(models.Model):
    """
    The hours in a day when an office is open
    """

    class DaysOfTheWeek(models.TextChoices):
        MONDAY = ("monday", _("Monday"))
        TUESDAY = ("tuesday", _("Tuesday"))
        WEDNESDAY = ("wednesday", _("Wednesday"))
        THURSDAY = ("thursday", _("Thursday"))
        FRIDAY = ("friday", _("Friday"))
        SATURDAY = ("saturday", _("Saturday"))
        SUNDAY = ("sunday", _("Sunday"))

    openfrom = models.TimeField(verbose_name=_("Open from"),)
    closedafter = models.TimeField(verbose_name=_("Closed after"),)
    dayofweek = models.CharField(
        max_length=20, choices=DaysOfTheWeek.choices, verbose_name=_("Day of the week"),
    )
