from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import User
from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):
    #delete the def __init__ if you want to provide help text
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = ("username","email","role","branch", "password1", "password2")


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("email","role")