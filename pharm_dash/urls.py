from django.urls import path
from pharm_dash import views

urlpatterns = [
    path('pharmdash', views.pharmdash, name="pharmdash"),
    path('patientrecords', views.patientrecords, name="patientrecords"),
    path('searchpatient', views.searchpatient, name="searchpatient"),
    
    path('medicalrecords/<patient_id>', views.medicalrecords, name="medicalrecords"),

    path('addpatient', views.addpatient, name="addpatient"),
    
]
