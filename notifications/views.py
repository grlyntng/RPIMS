from django.shortcuts import render
from .models import Notification
from .utils import check_notifications
# Create your views here.
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.template import loader
from django.contrib import messages 

#from .models import

def adminnotification(request):
    check_notifications() 
    notifications = Notification.objects.all()
    return render(request, 'notifications/adminnotification.html',{'notifications': notifications})

def pharmacistnotification(request):
    return render(request, 'notifications/pharmacistnotification.html')

def assistantnotification(request):
    return render(request, 'notifications/assistantnotification.html')
