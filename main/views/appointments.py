from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from main.views.file_upload import pdf_registry
from django.contrib.auth.models import User
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

    print("User calendar")
    return render(request, 'main/calendar.html')


