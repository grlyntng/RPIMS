from django.forms import ModelForm
from .widgets import DatePickerInput
from .models import Patient, Medical_Record

class addpatientform(ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['branch'].initial = user.branch #auto branch option to current branch
        for field in self.fields.values():
            field.help_text = ''
    class Meta:
        model = Patient
        fields = (
            'Patient_Name',
            'Age',
            'Phone', 
            'branch',           
        )

        labels = {
            'Patient_Name' : 'NAME',
            'Age':'AGE',
            'Phone':'PHONE',
            'branch':'BRANCH', 
        }

class addmedicalrecordform(ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['branch'].initial = user.branch #auto branch option to current branch
        for field in self.fields.values():
            field.help_text = ''
            
    model=Medical_Record
    fields = (
        'Examination_date',
        'Diagnosis',
        'Treatment',
        'patient',
    )

    widgets={
        'Examination_date':DatePickerInput(),
    }