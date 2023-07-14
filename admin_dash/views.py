from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.template import loader
from django.contrib import messages 

from .models import Branch_Location
from .forms import addbranchform, editbranchform


from users.models import User
from users.forms import CustomUserCreationForm


from assist_dash.models import Product

from calendar_module.models import Appointment
from django.db.models import Q

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

def searchinventories(request):
    if request.method == "POST":
        branch = request.POST.get('branch')
        category = request.POST.get('prod_cat')
        sortorder = request.POST.get('prod_columns')
        searched = request.POST['searched']
        products = Product.objects.all()
        mybranches = Branch_Location.objects.all()

        if branch != "all":
            products = products.filter(branch__Branch_Name=branch)

        if searched != "":
            search_filters = Q(Product_Name__icontains=searched) | Q(Product_Category__icontains=searched) | Q(Brand__icontains=searched) | Q(Form__icontains=searched) | Q(Unit_Dose__icontains=searched) | Q(Product_Quantity__icontains=searched)
            products = products.filter(search_filters)

        if category != "all":
            products = products.filter(Product_Category__icontains=category)

        if sortorder == "name-asc":
            products = products.order_by('Product_Name')
        elif sortorder == "name-desc":
            products = products.order_by('-Product_Name')
        elif sortorder == "exp-date-asc":
            products = products.order_by('Product_Expirydate')
        elif sortorder == "exp-date-desc":
            products = products.order_by('-Product_Expirydate')
        elif sortorder == "qty-asc":
            products = products.order_by('Product_Quantity')
        elif sortorder == "qty-desc":
            products = products.order_by('-Product_Quantity')
        else:
            products = products.order_by('Product_Name')

        return render(request, 'admin_dash/searchinventories.html', {'searched': searched, 'products': products, 'mybranches': mybranches})


def inventories(request):
    myproducts = Product.objects.all().order_by('Product_Expirydate')
    mybranches = Branch_Location.objects.all()

    template = loader.get_template('admin_dash/inventories.html')
    context = {
        'myproducts': myproducts,
        'mybranches': mybranches,
    }
    return HttpResponse(template.render(context,request))
        

from django.utils import timezone
from calendar import monthrange
from calendar_module.models import Appointment

from django.http import QueryDict

def calendars(request, year=None, month=None):
    mybranches = Branch_Location.objects.all()
    current_date = timezone.now()
    current_year = current_date.year if not year else int(year)
    current_month = current_date.month if not month else int(month)

    _, num_days = monthrange(current_year, current_month)
    num_days_list = list(range(1, num_days + 1))

    # Retrieve branch from query parameters
    branch = request.GET.get('branch')
    if branch:
        if branch != "all":
            appointments = Appointment.objects.filter(date__year=current_year, date__month=current_month, branch__Branch_Name=branch)
        else:
            appointments = Appointment.objects.filter(date__year=current_year, date__month=current_month)
    else:
        appointments = Appointment.objects.filter(date__year=current_year, date__month=current_month)

    year_choices = list(range(current_year - 5, current_year + 6))  # Example: Show 5 years in the past and future
    month_choices = list(range(1, 13))  # Show all months from 1 to 12

    # Calculate the number of empty cells before the first day of the month
    _, first_weekday = monthrange(current_year, current_month)
    empty_cells = ["-"] * first_weekday

    # Calculate the number of empty cells after the last day of the month
    last_weekday = (first_weekday + num_days) % 7
    empty_cells_end = ["-"] * (6 - last_weekday) if last_weekday != 6 else []

    num_days_list = empty_cells + num_days_list + empty_cells_end

    # Remove the first four rows of empty cells
    num_days_list = num_days_list[28:]

    context = {
        'mybranches': mybranches,
        'year': current_year,
        'month': current_month,
        'num_days': num_days_list,
        'appointments': appointments,
        'year_choices': year_choices,
        'month_choices': month_choices,
    }

    return render(request, 'admin_dash/calendars.html', context)
