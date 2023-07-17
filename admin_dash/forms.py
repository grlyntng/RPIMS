from django.forms import ModelForm 
from django import forms 
from .models import Branch_Location


class addbranchform(ModelForm):
    class Meta:
        model = Branch_Location
        fields = (
            'Branch_Name',
            'Branch_address',
            'Branch_state',
            'Branch_phonenumber'
        )
        labels = {
            'Branch_address':'Address',
            'Branch_state':'State',
            'Branch_phonenumber':'Phone',
        }

class editbranchform(ModelForm):
    def __init__(self, *args, **kwargs):
        super(editbranchform, self).__init__(*args, **kwargs)

        for fieldname in ['Branch_address']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = Branch_Location
        fields = (
            'Branch_phonenumber',
            'Branch_address',
        )
        labels = {
            'Branch_phonenumber':'PHONE',
            'Branch_address':'ADDRESS',
        }