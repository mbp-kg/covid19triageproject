from django import forms
from django.core.exceptions import ValidationError


class StrictBooleanField(forms.Field):
    def to_python(self, value):
        if value in (True, "True", "true", 1):
            return True
        elif value in (False, "False", "false", 0):
            return False
        else:
            raise ValidationError(self.error_messages["required"])
