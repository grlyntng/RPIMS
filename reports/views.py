from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.template import loader
from django.contrib import messages 

#for data visualization
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import pyplot
import json
import plotly
import plotly.express as px

#import models to be used in analytics and reports
from assist_dash.models import Product,Supplier

def adminreports(request): #take input later. this one just takes overall

    return render(request,'reports/admin-reports.html')

def pharmacistreports(request):
    return render(request, 'reports/pharmacist-reports.html')




