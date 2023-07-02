from django.forms import ModelForm 
from .widgets import DatePickerInput,TimePickerInput
from .models import Appointment

class AppointmentForm(ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['branch'].initial = user.branch #auto branch option to current branch
        for field in self.fields.values():
            field.help_text = ''
            
    class Meta:
        model = Appointment
        fields = (
            'app_detail',
            'date',
            'time_start',
            'branch',
        )

        labels = {
            'app_detail' : 'APPOINTMENT NAME',
            'date':'DATE',
            'time_start':'TIME',
            'branch':'BRANCH',
        }

        widgets={
            'date' : DatePickerInput(),
            'time_start': TimePickerInput(),
        }
