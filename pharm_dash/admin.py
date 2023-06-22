from django.contrib import admin

# Register your models here.
from .models import Patient
admin.site.register(Patient)

from .models import Medical_Record
admin.site.register(Medical_Record)