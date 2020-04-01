from django import forms
from django.utils.translation import pgettext_lazy


class KnownNullBooleanSelect(forms.Select):
    def __init__(self, attrs=None):
        choices = (
            (
                "unknown",
                pgettext_lazy("empty option for select button", "-----"),
            ),
            ("true", pgettext_lazy("true option for select button", "Yes")),
            ("false", pgettext_lazy("false option for select button", "No")),
        )
        super().__init__(attrs, choices)
