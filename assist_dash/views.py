from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.template import loader

from .models import Supplier,Order_Stock,Product
from .forms import addsupplierform, editsupplierform, placeorderform, addproductform
# Create your views here.

def assistdash(request):
    return render(request, 'assist_dash/assistdash.html')

def suppliers(request):
    mysuppliers = Supplier.objects.all()
    template = loader.get_template('assist_dash/suppliers.html')
    context = {
        'mysuppliers': mysuppliers
    }
    return HttpResponse(template.render(context,request))

def searchsupplier(request):
    if request.method == "POST":
        searched = request.POST['searched'] #get what the user searched for
        #returned searched results 
        suppliers = Supplier.objects.filter(Supplier_Name__contains=searched) or Supplier.objects.filter( Supplier_Phone__exact=searched ) or Supplier.objects.filter( Supplier_Email__contains=searched ) or Supplier.objects.filter( Supplier_Description__contains=searched ) 
        return render(request,'assist_dash/searchsupplier.html',{'searched':searched, 'suppliers':suppliers})
    else:
        return render(request,'assist_dash/searchsupplier.html')

def addsupplier(request):
        submitted = False
        if request.method == "POST":
            form = addsupplierform(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/addsupplier?submitted=True')
        else:
            form = addsupplierform
            if 'submitted' in request.GET:
                submitted = True
        
        form = addsupplierform
        return render(request,'assist_dash/addsupplier.html', {'form':form, 'submitted':submitted})


def orders(request):
    myorders = Order_Stock.objects.all()
    template = loader.get_template('assist_dash/orders.html')
    context = {
        'myorders': myorders
    }
    return HttpResponse(template.render(context,request))


def editsupplier(request,supplier_id):
    supplier_to_edit = Supplier.objects.get(pk=supplier_id)
    submitted = False
    form2 = editsupplierform(request.POST or None, instance=supplier_to_edit)
    template = loader.get_template('assist_dash/editsupplier.html')
    context = {
        'form2':form2,
        'supplier_to_edit': supplier_to_edit
    }
    return HttpResponse(template.render(context,request))

def placeorder(request):
        submitted = False
        if request.method == "POST":
            form3 = placeorderform(request.POST)
            if form3.is_valid():
                form3.save()
                return HttpResponseRedirect('/placeorder?submitted=True')
        else:
            form3 = placeorderform
            if 'submitted' in request.GET:
                submitted = True
        
        form3 = placeorderform
        return render(request,'assist_dash/placeorder.html', {'form':form3, 'submitted':submitted})


def searchorder(request):
    if request.method == "POST":
        searched = request.POST['searched'] #get what the user searched for
        #returned searched results 
        orders = Order_Stock.objects.filter(Order_Name__contains=searched) or Order_Stock.objects.filter( Order_Date__exact=searched ) or Order_Stock.objects.filter( supplier__contains=searched ) or Order_Stock.objects.filter( status__contains=searched ) 
        return render(request,'assist_dash/searchorder.html',{'searched':searched, 'orders':orders})
    else:
        return render(request,'assist_dash/searchorder.html')
    

def inventory(request):
    myproducts = Product.objects.all()
    template = loader.get_template('assist_dash/inventory.html')
    context = {
        'myproducts': myproducts
    }
    return HttpResponse(template.render(context,request))

def addproduct(request):
        submitted = False
        if request.method == "POST":
            form4 = addproductform(request.POST)
            if form4.is_valid():
                form4.save()
                return HttpResponseRedirect('/addproduct?submitted=True')
        else:
            form4 = addproductform
            if 'submitted' in request.GET:
                submitted = True
        
        form4 = addproductform
        return render(request,'assist_dash/addproduct.html', {'form':form4, 'submitted':submitted})

def searchproduct(request):
    if request.method == "POST":
        searched = request.POST['searched'] #get what the user searched for
        #returned searched results 
        products = Product.objects.filter(Product_Name__contains=searched) or Product.objects.filter(Product_Quantity__exact=searched) or Product.objects.filter(Product_Category__contains=searched) or Product.objects.filter(Brand__contains=searched) or Product.objects.filter(Form__contains=searched) or Product.objects.filter(Unit_Dose_contains=searched)
        return render(request,'assist_dash/searchproduct.html',{'searched':searched, 'products':products})
    else:
        return render(request,'assist_dash/searchproduct.html')
    


