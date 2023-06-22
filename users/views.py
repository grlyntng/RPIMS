from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from django.http import HttpResponse 
from .models import User

# Create your views here.
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password=password)
        if user is not None:
            login(request,user)
            #redirect to a successpage
            if user.role == ("ADMIN"):
                return redirect('adminnotification')
            elif user.role == ("ASSISTANT"):
                return redirect('assistantnotification')
            else: 
                return redirect('pharmacistnotification')
        else:
            messages.error(request, ("That wasn't right. Please try again"))
            return redirect('login_user')
    else:
        return render(request,'authenticate/login.html',{})
    

def logout_user(request):
    logout(request)
    messages.success(request, ("You've been logged out :)"))
    return redirect('login_user')
