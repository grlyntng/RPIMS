from django.urls import path
from reports import views

urlpatterns = [
    path('adminreports', views.adminreports, name="adminreports"),
    path('pharmacistreports', views.pharmacistreports, name="pharmacistreports"),
]
