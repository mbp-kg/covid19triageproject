import datetime

from django.test import TestCase
from pytz import timezone

from .api import is_open


class WorkingHoursTests(TestCase):
    def test_monday_ten_am(self):
        tz = timezone("Asia/Bishkek")
        testinput = datetime.datetime(2020, 3, 30, 10, 0, tzinfo=tz)
        self.assertTrue(is_open(testinput))

    def test_sunday_ten_am(self):
        tz = timezone("Asia/Bishkek")
        testinput = datetime.datetime(2020, 3, 29, 10, 0, tzinfo=tz)
        self.assertFalse(is_open(testinput))

    def test_other_timezone(self):
        tz = timezone("America/Chicago")
        testinput = datetime.datetime(2020, 3, 31, 10, 0, tzinfo=tz)
        self.assertFalse(is_open(testinput))
