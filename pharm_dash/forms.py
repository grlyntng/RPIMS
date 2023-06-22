from django.forms import ModelForm
from .widgets import DatePickerInput
from .models import Patient, Medical_Record

class addpatientform(ModelForm):
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