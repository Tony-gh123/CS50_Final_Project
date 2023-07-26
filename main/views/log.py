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
from pdfminer.high_level import extract_text
import logging
import os


# Create your views here.

def index(request):
    return render(request, 'main/land.html')

def home(request):
    return render(request, "main/home.html")

def logout_user(request):
    
    logout(request)
    messages.success(request, ("Logout sucessfull"))
    return redirect('home')

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('login')
    else:
        return render(request, 'main/login.html', {})

def signup(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # save user's account as user
            user = form.save()

            # Get the user's email from the form
            email = form.cleaned_data.get('email')

            # Create a UserUploads instance and associate it with the user
            UserUploads.objects.create(user=user)

            return redirect('login')
        else:
            print(form.errors)
    else:
        form = UserCreationForm()
    return render(request, 'main/signup.html', {'form':form,})

@login_required
def pdf_registry(request): # Upload, Display and Delete pdf files!
    
    try:
        #fetch users uploaded pdfs
        user_pdfs = UserUploads.objects.filter(user=request.user)

        if request.method == 'POST':
            if 'pdf_upload' in request.FILES:
                #get pdf file from user_profile.html
                pdf_file = request.FILES.get('pdf_upload')

                #Create a new UserUploads instance for the current user and upload file
                user_upload = UserUploads(user=request.user, pdf_file=pdf_file)
                user_upload.save()

                return redirect('pdf_registry')

            elif 'pdf_delete' in request.POST:
                pdf_delete_ids = request.POST.getlist('pdf_delete')
                UserUploads.objects.filter(id__in=pdf_delete_ids, user=request.user).delete()

                return redirect('pdf_registry')

        return render(request, 'main/user_profile.html', {'user_pdfs': user_pdfs})

    except UserUploads.DoesNotExist as e:
        logging.error(f"UserUploads.DoesNotExist: {e}")
        return render(request, 'main/home.html', {'error_message': "Error Occurred"})
    
    return render(request, 'main/user_profile.html')


#Define a signal receiver to handle file deletion before the model is deleted
@receiver(pre_delete, sender=UserUploads)
def delete_vscode_file(sender, instance, **kwargs):
    # Get path to the file in the media folder
    file_path = instance.pdf_file.path

    #Delete the file from the file system
    if os.path.exists(file_path):
        os.remove(file_path)


"""
Unapplied pdf extract feature - changed project idea

urls.py
path('extract/', pdf_extract, name='pdf_extract')

land.html (nav-bar)
<li class="nav-item">
    <a class="nav-link" href="/extract">PDF EXtract</a>
</li>

views.py
@login_required
def pdf_extract(request):

    try:
        if request.method == 'POST':
            
            pdf_ids = request.POST.getlist('pdf_extract')
        
        user_pdfs = UserUploads.objects.filter(user=request.user)
        return render(request, 'main/extract.html', {'user_pdfs': user_pdfs})

    except Exception as e:
        return render(request, 'main/home.html', {'error_message': "Error Occurred" + str(e)})
    
    return render(request, 'main/extract.html')
"""