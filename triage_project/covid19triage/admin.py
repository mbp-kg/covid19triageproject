from django.contrib import admin

from .models import Assessment
from .models import AssessmentLog
from .models import ContactPerson
from .models import Patient
from .models import PatientFactors

admin.site.register(Assessment)
admin.site.register(AssessmentLog)
admin.site.register(ContactPerson)
admin.site.register(Patient)
admin.site.register(PatientFactors)
