from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.template import loader

from .models import Patient, Medical_Record

from .forms import addpatientform, addmedicalrecordform


# Create your views here.
def pharmdash(request):
    return render(request,'pharm_dash/pharmdash.html')

def patientrecords(request):
    mypatients = Patient.objects.all()
    template = loader.get_template('pharm_dash/patientrecords.html')
    context={
        'mypatients' : mypatients
    }
    return HttpResponse(template.render(context,request))

def searchpatient(request):
    if request.method == "POST":
        searched = request.POST['searched'] #get what the user searched for
        #returned searched results 
        patients = Patient.objects.filter(Patient_Name__contains=searched) or Patient.objects.filter( Phone__exact=searched ) or Patient.objects.filter( Age__exact=searched ) 
        return render(request,'pharm_dash/searchpatient.html',{'searched':searched, 'patients':patients})
    else:
        return render(request,'pharm_dash/searchpatient.html')


####################UPDATE########################
def medicalrecords(request,patient_id):
    patient_viewed = Patient.objects.get(pk=patient_id) #call object from database
    medicalrecords = Medical_Record.objects.all()
    template = loader.get_template('pharm_dash/medicalrecords.html')
    context = {
        'patient_viewed': patient_viewed,
        'medicalrecords': medicalrecords,
    }
    return HttpResponse(template.render(context,request))


def viewmedrecord(request): ## maybe change to editmedrecord?
    return render(request,'pharm_dash/medicalrecords.html') ##### UPDATE THIS TO NEW HTML

###################CREATE########################
def addpatient(request):
    submitted = False
    if request.method == "POST":
        form = addpatientform(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/addpatient?submitted=True')
    else:
        form = addpatientform
        if 'submitted' in request.GET:
            submitted = True
    
    form = addpatientform
    return render(request,'pharm_dash/addpatient.html', {'form':form, 'submitted':submitted})



