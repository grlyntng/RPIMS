from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.template import loader
from django.contrib import messages 

from .models import Branch_Location
from .forms import addbranchform, editbranchform


from users.models import User
from users.forms import CustomUserCreationForm

######################READ###########################
def admindash(request):
    return render(request, 'admin_dash/admindash.html')

def branches(request):
    mybranches = Branch_Location.objects.all().values()
    template = loader.get_template('admin_dash/branches.html')
    context = {
        'mybranches': mybranches
    }
    return HttpResponse(template.render(context,request))

def roles(request):
    myusers = User.objects.all()
    template = loader.get_template('admin_dash/roles.html')
    context = {
        'myusers': myusers
    }
    return HttpResponse(template.render(context,request))

####################CREATE##########################
def addbranch(request):
    submitted = False
    if request.method == "POST":
        form = addbranchform(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/addbranch?submitted=True')
    else:
        form = addbranchform
        if 'submitted' in request.GET:
            submitted = True
    
    form = addbranchform
    return render(request,'admin_dash/addbranch.html', {'form':form, 'submitted':submitted})

def adduser(request):
    submitted = False
    if request.method == "POST":
        form2 = CustomUserCreationForm(request.POST)
        if form2.is_valid():
            form2.save()
            return HttpResponseRedirect('/adduser?submitted=True')
        else:
            messages.error(request, ("That wasn't right. Please try again"))
    else:
        form2 = CustomUserCreationForm
        if 'submitted' in request.GET:
            submitted = True
    
    form2 = CustomUserCreationForm
    return render(request,'admin_dash/adduser.html', {'form':form2, 'submitted':submitted})


####################UPDATE########################
def viewbranch(request,branch_id):
    branch_to_edit = Branch_Location.objects.get(pk=branch_id) #call object from database
    submitted = False
    form3 = editbranchform(request.POST or None, instance=branch_to_edit)

    return render(request,'admin_dash/viewbranch.html',{'branch_to_edit': branch_to_edit,
        'form3' : form3,
        'submitted':submitted,})

def viewuser(request,user_id):
    user_viewed = User.objects.get(pk=user_id) #call object from database
    template = loader.get_template('admin_dash/viewuser.html')
    context = {
        'user_viewed': user_viewed
    }
    return HttpResponse(template.render(context,request))


####################DELETE############################
def deleteuser(request,user_id):
    user_to_delete = User.objects.get(pk=user_id) #call object from database
    user_to_delete.delete()
    return redirect('admin_dash/roles.html')

def deletebranch(request,branch_id):
    branch_to_delete = User.objects.get(pk=branch_id) #call object from database
    branch_to_delete.delete()
    return redirect('admin_dash/branches.html')