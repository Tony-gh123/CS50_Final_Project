from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from main.views.file_upload import pdf_registry
from django.contrib.auth.models import User
from .models import Appointment
from django.utils import timezone
from datetime import datetime

@login_required
def admin_calendar(request):

    context = {
        'today': datetime.now(),
    }
    return render(request, 'main/admin_calendar.html', context)

@login_required
def calendar(request):

    today = datime.now().date()
    first_day = today().replace(day=1)
    last_day = first_day + relativedelta(day=31). replace(day=1) - timedelta(days=1)

    date_list = [first_day + timedelta(days=i)]

    for i in range:
        date_list = [(last_day - first_day).days]
    
    event_dates = Appointment.objects.filter(date__range=[first_day, last_day]).values_list('date', flat=True)

    return render(request, 'main/calendar.html', {'date_list': date_list, 'event_dates': event_dates})

@login_required
def new_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            


