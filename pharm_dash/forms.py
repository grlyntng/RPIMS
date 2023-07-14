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

class addmedrecordform(ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['branch'].initial = user.branch
        self.fields['patient'].queryset = Patient.objects.filter(branch=user.branch)
        for field in self.fields.values():
            field.help_text = ''

    class Meta:        
        model=Medical_Record
        fields = (
            'Examination_Date',
            'Diagnosis',
            'Treatment',
            'patient',
            'branch',
        )

        labels = {
            'Examination_Date': 'EXAMINATION DATE',
            'Diagnosis':'DIAGNOSIS',
            'Treatment':'TREATMENT',
            'patient':'PATIENT',
            'branch':'BRANCH', 
        }

        widgets={
            'Examination_Date':DatePickerInput(),
        }