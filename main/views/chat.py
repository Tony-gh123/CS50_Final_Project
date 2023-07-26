from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.db import models
from main.models import UserUploads, Chat
from django.http import HttpResponse
import logging
import os


@login_required
def admin_chat(request):

    if not request.user.is_superuser:
        return redirect('main/home.html')

    users = User.objects.exclude(pk=request.user.pk)
    print(users)
    return render(request, 'main/admin_chat.html', {'users': users})

@login_required
def chat(request):

    conversation = Chat.objects.filter(sender=request.user) | Chat.objects.filter(recipient=request.user)
    return render(request, 'main/chat.html', {'view': 'chat', 'conversation': conversation})

@login_required
def send(request, recipient_id):

    recipient = get_object_or_404(User, pk=recipient_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        message = Message.objects.create(sender=request.user, recipient=recipient, content=content)

    return render(request, 'main/chat.html', {'view': 'send', 'recipient': recipient})


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