from django.forms import ModelForm 
from .widgets import DatePickerInput,TimePickerInput
from .models import Appointment

class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = (
            'app_detail',
            'date',
            'time_start',
            'time_end',
            'branch',
        )

        widgets={
            'date' : DatePickerInput(),
            'time_start': TimePickerInput(),
            'time_end': TimePickerInput(),
        }
