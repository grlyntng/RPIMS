from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.template import loader
from django.contrib import messages 

#from .models import

def adminnotification(request):
    return render(request, 'notifications/admin-notification.html')

def pharmacistnotification(request):
    return render(request, 'notifications/pharmacist-notification.html')

def assistantnotification(request):
    return render(request, 'notifications/assistant-notification.html')
