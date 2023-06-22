from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator #used to constrain phone number range
state_choices = (
    ("Johor","Johor"),
    ("Kedah","Kedah"),
    ("Kelantan","Kelantan"),
    ("Malacca","Malacca"),
    ("Negeri Sembilan","Negeri Sembilan"),
    ("Pahang","Pahang"),
    ("Penang","Penang"),
    ("Perak","Perak"),
    ("Perlis","Perlis"),
    ("Sabah","Sabah"),
    ("Sarawak","Sarawak"),
    ("Selangor","Selangor"),
    ("Terengganu","Terengganu"),
    ("Kuala Lumpur","Kuala Lumpur"),
    ("Labuan","Labuan"),
    ("Putrajaya","Putrajaya"),
    ("default","default"),
)

# Create your models here.
class Branch_Location(models.Model):
    #using the built in django id as pk
    #use view to call model then output template tag to concat via formatting when called
    Branch_Name = models.CharField(max_length=50, unique=True)
    Branch_address = models.CharField(max_length=255, unique=True)
    Branch_phonenumber = models.IntegerField(default = 1, validators=[MaxValueValidator(6000000000000), MinValueValidator(6000000000)])
    Branch_state = models.CharField(max_length = 20,choices = state_choices, default ='default')
    
    def __str__(self):
        return self.Branch_Name

