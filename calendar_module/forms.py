from django.forms import ModelForm 
from .widgets import DateTimePickerInput
from .models import Appointment

class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = (
            'app_detail',
            'datetime_start',
            'datetime_end',
            'branch',
        )

        widgets={
            'datetime_start' : DateTimePickerInput(),
            'datetime_end' : DateTimePickerInput(),
        }
