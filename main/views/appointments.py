from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from main.views.file_upload import pdf_registry
from django.contrib.auth.models import User
from main.models import Appointment, AppointmentForm
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta

@login_required
def admin_calendar(request):

    print('admin_calendar')
    return render(request, 'main/admin_calendar.html', context)

@login_required
def calendar(request):

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()
            return redirect('calendar')
        else:
            form = AppointmentForm()
    else:
        form = AppointmentForm()
    
    return render(request, 'main/calendar.html', {'form': form})
