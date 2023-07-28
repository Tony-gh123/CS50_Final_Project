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
from django.utils import timezone
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
        if 'chat_delete' in request.POST:
                chat_delete(request, recipient)
        messages = fetch_chat(request, recipient)
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
        if 'chat_delete' in request.POST:
                chat_delete(request, recipient)
        messages = fetch_chat(request, recipient)
    else:
        recipient = None
        messages = []

    return render(request, 'main/chat.html', {'admins': admins, 'recipient': recipient, 'messages': messages})

@login_required
def fetch_chat(request, recipient):
        
    return Chat.objects.filter(
        (models.Q(sender=request.user) & models.Q(recipient=recipient)) |
        (models.Q(recipient=request.user) & models.Q(sender=recipient)), 
        is_deleted=False
    ).order_by('timestamp')

@login_required
def chat_delete(request, recipient_id):

    recipient = get_object_or_404(User, pk=recipient_id)

    return Chat.objects.filter(
        (models.Q(sender=request.user) & models.Q(recipient=recipient)) |
        (models.Q(recipient=request.user) & models.Q(sender=recipient)), 
        is_deleted=False
    ).update(is_deleted=True, deleted_at=timezone.now())

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
def add_file(request, message_id):

    message = get_object_or_404(Chat, pk=message_id)

    if request.method == 'POST':
        #check if there is a file
        if message.file:
            #get pdf file from chat and upload
            download_file = UserUploads(user=request.user, pdf_file=message.file)
            download_file.save()

    if request.user == message.sender:
        url = reverse('conversation', args=[message.recipient.id])
    else:
        url = reverse('conversation', args=[message.sender.id])

    return HttpResponseRedirect(url)

