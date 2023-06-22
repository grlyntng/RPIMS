from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import AppointmentForm

# Register your models here.
from.models import Appointment


admin.site.register(Appointment)

