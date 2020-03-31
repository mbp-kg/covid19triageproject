from django.contrib import admin

from .models import Timezone
from .models import WorkDay

admin.site.register(Timezone)
admin.site.register(WorkDay)
