from django.urls import path,include
from calendar_module import views

urlpatterns = [
    path('calendar', views.calendar, name="calendar" ),

]
