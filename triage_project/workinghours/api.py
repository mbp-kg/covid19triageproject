import datetime

from pytz import timezone

from .models import Timezone
from .models import WorkDay


_weekdays = [
    WorkDay.DaysOfTheWeek.MONDAY,
    WorkDay.DaysOfTheWeek.TUESDAY,
    WorkDay.DaysOfTheWeek.WEDNESDAY,
    WorkDay.DaysOfTheWeek.THURSDAY,
    WorkDay.DaysOfTheWeek.FRIDAY,
    WorkDay.DaysOfTheWeek.SATURDAY,
    WorkDay.DaysOfTheWeek.SUNDAY,
]


def is_open(now: datetime.datetime):
    """
    Check to see if a datetime falss within working hours
    """
    tzname = Timezone.objects.first()
    tz = timezone(tzname.tz)
    nowsametz = now.astimezone(tz)
    today = _weekdays[nowsametz.weekday()]
    rightnow = nowsametz.time()
    workdays = WorkDay.objects.filter(
        dayofweek=today, openfrom__lt=rightnow, closedafter__gt=rightnow
    )
    return workdays.count() > 0
