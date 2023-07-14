from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.template import loader

from .models import Supplier,Order_Stock,Product, Sale, Sale_Detail
from .forms import addsupplierform, editsupplierform, placeorderform, addproductform, editorderform
from calendar_module.models import Appointment

from django.db.models import Q

def assistdash(request):
    return render(request, 'assist_dash/assistdash.html')

def order_confirmation(request, sale_id):
    sale = Sale.objects.get(id=sale_id)
    return render(request, 'assist_dash/order_confirmation.html', {'sale': sale})

def checkout(request):
    if request.method == 'POST':
         # Process form data
        sale_date = request.POST['sale_date']
        sale_method = request.POST['sale_method']
        
        # Retrieve the selected products and quantities
        selected_products = []
        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                product_id = key.split('_')[1]
                quantity = int(value)
                selected_products.append({'product_id': product_id, 'quantity': quantity})
        
        # Calculate sale total and quantity
        sale_total = 0
        quantity = 0
        for item in selected_products:
            product = Product.objects.get(id=item['product_id'])
            item_total = product.Product_Price * item['quantity']
            sale_total += item_total
            quantity += item['quantity']
        
        # Retrieve the selected product
        product = Product.objects.get(id=product_id)
        
        # Create sale
        sale = Sale.objects.create(
            Sale_total=sale_total,
            Sale_Date=sale_date,
            Sale_Method=sale_method,
            branch = request.user.branch,
        )
        
       # Create sale details for the selected products
        for item in selected_products:
            product = Product.objects.get(id=item['product_id'])
            Sale_Detail.objects.create(
                Item_Quantity=item['quantity'],
                product=product,
                sale=sale,
                branch = request.user.branch,
            )
        
        # Redirect to order confirmation page
        return redirect('order_confirmation', sale_id=sale.id)
    
    # If GET request or form is invalid, render the checkout template
    products = Product.objects.all()
    return render(request, 'assist_dash/checkout.html', {'products': products})            
  

def suppliers(request):
    mysuppliers = Supplier.objects.all()
    template = loader.get_template('assist_dash/suppliers.html')
    context = {
        'mysuppliers': mysuppliers
    }
    return HttpResponse(template.render(context,request))

def searchsupplier(request):
    if request.method == "POST":
        searched = request.POST.get('searched')
        mysuppliers = Supplier.objects.all()
        search_filters = Q(Supplier_Name__icontains=searched) |Q(Supplier_Phone__icontains=searched) |Q(Supplier_Email__icontains=searched) |Q(Supplier_Description__icontains=searched)
        mysuppliers = mysuppliers.filter(search_filters)
        return render(request, 'assist_dash/searchsupplier.html', {'searched': searched, 'mysuppliers': mysuppliers})
    else:
        return render(request, 'assist_dash/searchsupplier.html')

def addsupplier(request):
        submitted = False
        if request.method == "POST":
            form5 = addsupplierform(request.POST)
            if form5.is_valid():
                form5.save()
                return HttpResponseRedirect('/addsupplier?submitted=True')
        else:
            form5 = addsupplierform(user=request.user)
            if 'submitted' in request.GET:
                submitted = True
        return render(request,'assist_dash/addsupplier.html', {'form5':form5, 'submitted':submitted})


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
            form3 = placeorderform(user=request.user, data=request.POST)
            if form3.is_valid():
                form3.save() #save the Order_Stock object

                #getting data from the form entry
                appdetaildata = form3.cleaned_data.get('Order_Name') 
                appdatedata = form3.cleaned_data.get('Order_Date')
                apptimedata = form3.cleaned_data.get('Order_Time')

                #creating a new object from form data in Appointment
                Appointment.objects.create(app_detail = appdetaildata, date = appdatedata, time_start = apptimedata, branch = request.user.branch )
                return HttpResponseRedirect('/placeorder?submitted=True')
        else:
            form3 = placeorderform(user=request.user)
            if 'submitted' in request.GET:
                submitted = True
        return render(request,'assist_dash/placeorder.html', {'form':form3, 'submitted':submitted})


def searchorder(request):
    if request.method == "POST":
        status = request.POST.get('status')
        sortby = request.POST.get('sortby')
        searched = request.POST['searched']
        myorders = Order_Stock.objects.all()

        if searched !="":
            search_filters = Q(Order_Name__icontains=searched) | Q(Order_Quantity__icontains=searched) | Q(Order_Total__icontains=searched) | Q(Order_Status__icontains=searched) | Q(supplier__icontains=searched) 
            myorders = myorders.filter(search_filters)

        if status !="ALL":
            myorders = myorders.filter(Order_Status__icontains=status)

        if sortby == "date-asc":
            myorders = myorders.order_by('Order_Date')
        else:
            myorders = myorders.order_by('-Order_Date')
            
        return render(request, 'assist_dash/searchorder.html', {'searched': searched, 'myorders': myorders})
    
    return render(request,'assist_dash/orders.html')
    

def inventory(request):
    myproducts = Product.objects.all().order_by('Product_Expirydate')
    template = loader.get_template('assist_dash/inventory.html')
    context = {
        'myproducts': myproducts
    }
    return HttpResponse(template.render(context,request))

def addproduct(request):
        submitted = False
        if request.method == "POST":
            form4 = addproductform(user=request.user, data=request.POST)
            if form4.is_valid():
                form4.save()
                return HttpResponseRedirect('/addproduct?submitted=True')
        else:
            form4 = addproductform(user=request.user)
            if 'submitted' in request.GET:
                submitted = True
        return render(request,'assist_dash/addproduct.html', {'form':form4, 'submitted':submitted})


def searchproduct(request):
    if request.method == "POST":
        category = request.POST.get('prod_cat')
        sortorder = request.POST.get('prod_columns')
        searched = request.POST['searched']
        products = Product.objects.all()

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

        return render(request, 'assist_dash/searchproduct.html', {'searched': searched, 'products': products})

    return render(request, 'assist_dash/inventory.html')
        

from django.core.exceptions import ValidationError

def vieworder(request, id):
    order_to_edit = Order_Stock.objects.get(pk=id)  # Call object from the database
    submitted = False

    if request.method == 'POST':
        form = editorderform(request.POST, instance=order_to_edit)
        if form.is_valid():
            form.save()
            submitted = True
            success_message = "Order has been successfully updated."
    else:
        form = editorderform(instance=order_to_edit)

    return render(request, 'assist_dash/vieworder.html', {
        'order_to_edit': order_to_edit,
        'form': form,
        'submitted': submitted,
        'success_message': success_message if submitted else None,
    })
