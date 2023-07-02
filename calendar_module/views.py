from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.template import loader
from django.utils import timezone
from calendar import monthrange
from .models import Appointment
from .forms import AppointmentForm


def calendar(request, year=None, month=None):
    current_date = timezone.now()
    current_year = current_date.year if not year else int(year)
    current_month = current_date.month if not month else int(month)

    _, num_days = monthrange(current_year, current_month)
    num_days_list = list(range(1, num_days + 1))

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
        'year': current_year,
        'month': current_month,
        'num_days': num_days_list,
        'appointments': appointments,
        'year_choices': year_choices,
        'month_choices': month_choices,
    }


    return render(request, 'calendar_module/calendar.html', context)

def addappointment(request):
        submitted = False
        if request.method == "POST":
            form = AppointmentForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/addappointment?submitted=True')
        else:
            form = AppointmentForm(user=request.user)
            if 'submitted' in request.GET:
                submitted = True
        return render(request,'calendar_module/addappointment.html', {'form':form, 'submitted':submitted})

