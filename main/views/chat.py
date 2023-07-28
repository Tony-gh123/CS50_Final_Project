from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.db import models
from main.models import UserUploads, Chat
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
import logging
import os


@login_required
def admin_chat(request):

    if not request.user.is_superuser:
        return redirect('main/home.html')

    users = User.objects.exclude(pk=request.user.pk)
    
    recipient_id = request.GET.get('recipient_id')

    if recipient_id:
        recipient = get_object_or_404(User, pk=recipient_id)
        messages = Chat.objects.filter(
        (models.Q(sender=request.user) & models.Q(recipient=recipient)) |
        (models.Q(recipient=request.user) & models.Q(sender=recipient))
    ).order_by('timestamp')
    else:
        recipient = None
        messages = []

    return render(request, 'main/admin_chat.html', {'users': users, 'recipient': recipient, 'messages': messages})

@login_required
def chat(request):

    admins = User.objects.filter(is_superuser=True)
    
    recipient_id = request.GET.get('recipient_id')

    if recipient_id:
        recipient = get_object_or_404(User, pk=recipient_id)
        messages = Chat.objects.filter(
        (models.Q(sender=request.user) & models.Q(recipient=recipient)) |
        (models.Q(recipient=request.user) & models.Q(sender=recipient))
    ).order_by('timestamp')
    else:
        recipient = None
        messages = []

    return render(request, 'main/chat.html', {'admins': admins, 'recipient': recipient, 'messages': messages})

@login_required
def send(request, recipient_id):

    recipient = get_object_or_404(User, pk=recipient_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        file = request.FILES.get('file')
        message = Chat.objects.create(sender=request.user, recipient=recipient, content=content, file=file)

    if request.user.is_superuser:
        url = reverse('admin_chat') + f'?recipient_id={recipient_id}'
    else:
        url = reverse('chat') + f'?recipient_id={recipient_id}'

    return HttpResponseRedirect(url)


@login_required
def conversation(request, recipient_id):

    recipient = get_object_or_404(User, pk=recipient_id)

    messages = Chat.objects.filter(
        (models.Q(sender=request.user) & models.Q(recipient=recipient)) |
        (models.Q(recipient=request.user) & models.Q(sender=recipient))
    ).order_by('timestamp')

    if not messages:
        messages = Chat.objects.none()

    return render(request, 'main/chat.html', {'view': 'conversation', 'recipient': recipient, 'messages': messages})