from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from main.views.file_upload import pdf_registry
from django.contrib.auth.models import User
from main.models import Appointment, AppointmentForm
from django.db.models import Q
from datetime import timedelta


@login_required
def calendar(request):

    if request.user.is_staff:
        user_appointments = Appointment.objects.filter(admin=request.user)
    else:
        user_appointments = Appointment.objects.filter(user=request.user)

    if request.method == "POST":
        action = request.POST.get('action')
        if action == "cancel":
                appointment_id = request.POST.get('appointment_id')
                appointment = get_object_or_404(Appointment, id=appointment_id)
                appointment.status = 'cancelled'
                appointment.save()

    context = {
        'appointments': user_appointments
    }

    return render(request, 'main/calendar.html', context)

@login_required
def new_apt(request):

    # define users and admins.
    users = None
    admins = None

    if request.user.is_staff:
        user_appointments = Appointment.objects.filter(admin=request.user)
        users = User.objects.filter(is_staff=False, is_superuser=False)
    else:
        user_appointments = Appointment.objects.filter(user=request.user)
        admins = User.objects.filter(is_staff=True)

    form = AppointmentForm()

    if request.method == "POST":
        action = request.POST.get('action')
        if action == "save":
            form = AppointmentForm(request.POST)
            if form.is_valid():
                recipient_id = request.POST.get('recipient')
                recipient = User.objects.get(pk=recipient_id)
                appointment = form.save(commit=False)
                if request.user.is_staff:
                    appointment.admin = request.user
                    appointment.user = recipient
                else:
                    appointment.user = request.user
                    appointment.admin = recipient
                appointment.save()
            else:
                print("Invalid Form")
                print("Form Errors:", form.errors)

        elif action == "dismiss":
            form = AppointmentForm()
    
    context = {
        'form': form,
        'users': users,
        'admins': admins,
    }
    
    return render(request, 'main/new_apt.html', context)

@login_required
def previous_apts(request):

    appointments = Appointment.objects.filter( Q(user=request.user) | Q(admin=request.user),
    status__in=['cancelled', 'completed'])

    if request.method == "POST":
        if request.POST.get('action') == "previous_apts":
            return render(request, 'main/previous_apts.html', {'appointments': appointments})

        elif request.POST.get('action') == "restore":
            appointment_id = request.POST.get('restore')
            try:
                appointment = Appointment.objects.get(id=appointment_id)
                appointment.status = 'scheduled'
                appointment.save()
            except Appointment.DoesNotExist:
                print("failed to reschedule")

    return render(request, 'main/previous_apts.html', {'appointments': appointments})
