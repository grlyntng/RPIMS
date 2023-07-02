from django.urls import path,include
from calendar_module import views
from .views import calendar,addappointment

urlpatterns = [
    path('calendar', calendar, name="calendar" ),
    path('calendar/<int:year>/<int:month>/', calendar, name='calendar_month'),
    path('addappointment', views.addappointment, name="addappointment" ),
]
