from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from main.views.file_upload import pdf_registry
from django.contrib.auth.models import User
from main.models import Appointment, AppointmentForm
from django.db.models import Q

@login_required
def calendar(request):

    admins = User.objects.filter(is_staff=True)
    appointments = Appointment.objects.filter(Q(user=request.user) | Q(admin=request.user))

    form = AppointmentForm()

    if request.method == "POST":
        action = request.POST.get('action')
        if action == "save":
            form = AppointmentForm(request.POST)
            if form.is_valid():
                    appointment = form.save(commit=False)
                    appointment.user = request.user
                    appointment.save()
                    return redirect('calendar')
            else:
                print("Invalid Form")
                print("Form Errors:", form.errors)

        elif action == "dismiss":
            form = AppointmentForm()
        
        elif action == "cancel":
            appointment_id = request.POST.get('appointment_id')
            appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)
            appointment.status = 'cancelled'
            appointment.save()
    else:
        form = AppointmentForm()
    
    return render(request, 'main/calendar.html', {'form': form, 'appointments': appointments, 'admins': admins})


@login_required
def previous_apts(request):

    appointments = Appointment.objects.filter(Q(user=request.user) | Q(admin=request.user),
    status__in=['cancelled', 'completed'])

    print(appointments)

    if request.method == "POST" and request.POST.get('action') == "previous_apts":
        return render(request, 'main/previous_apts.html', {'appointments': appointments})

    return render(request, 'main/calendar.html', {'appointments': appointments})
