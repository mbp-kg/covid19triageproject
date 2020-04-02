from django.contrib import admin

from .models import ContactPerson
from .models import Patient
from .models import PatientFactors

admin.site.register(ContactPerson)
admin.site.register(Patient)
admin.site.register(PatientFactors)
