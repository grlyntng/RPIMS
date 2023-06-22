from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator #used to constrain age range
from admin_dash.models import Branch_Location


# Create your models here.
class Patient(models.Model):
    #using the built in django id as pk
    Patient_Name = models.CharField(max_length=100)
    Age = models.IntegerField(default = 1, validators=[MaxValueValidator(150), MinValueValidator(1)])
    Phone = models.IntegerField(default = 1, validators=[MaxValueValidator(6000000000000), MinValueValidator(6000000000)])
    branch = models.ForeignKey(Branch_Location, on_delete=models.CASCADE, default = "1")
    def __str__(self):
        return self.Patient_Name

class Medical_Record(models.Model):
    #using the built in django id as pk
    Examinination_Date = models.DateField(null=True)
    Diagnosis = models.TextField(max_length=255)
    Treatment = models.TextField(max_length=255)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, default = "1")
    branch = models.ForeignKey(Branch_Location, on_delete=models.CASCADE, default = "1")
    def __str__(self):
        return self.Diagnosis

