from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.template import loader

from .models import Appointment

# Create your views here.
def calendar(request):
    myappointments = Appointment.objects.all()
    template = loader.get_template('calendar_module/calendar.html')
    context = {
        'myappointments': myappointments
    }
    return HttpResponse(template.render(context,request))

