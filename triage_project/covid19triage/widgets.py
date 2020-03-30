from django import forms
from django.utils.translation import pgettext_lazy


class KnownNullBooleanSelect(forms.Select):

    def __init__(self, attrs=None):
        choices = (
            ("unknown", pgettext_lazy("empty option for select button", "-----")),
            ("true", pgettext_lazy("true option for select button", "Yes")),
            ("false", pgettext_lazy("false option for select button", "No")),
        )
        super().__init__(attrs, choices)

    def format_value(self, value):
        try:
            return {
                True: "true", False: "false",
                "true": "true", "false": "false",
                "2": "true", "3": "false",
            }[value]
        except KeyError:
            return "unknown"

    def value_from_data_dict(self, data, files, name):
        value = data.get(name)
        return {
            True: True,
            "true": True,
            "True": True,
            False: False,
            "false": False,
            "False": False,
        }.get(value)
