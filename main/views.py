from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import UserUploads
import logging


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
def pdf_upload_display(request):
    
    try:
        if request.method == 'POST':
            #get pdf file from user_profile.html
            pdf_file = request.FILES.get('pdf_file')

            #Create a new UserUploads instance for the current user and upload file
            user_upload = UserUploads(user=request.user, pdf_file=pdf_file)
            user_upload.save()

            redirect(reverse('pdf_upload_display'))

            #Get all UserUpload instances for the current user
        user_pdfs = UserUploads.objects.filter(user=request.user)
        return render(request, 'main/user_profile.html', {user_pdfs: user_pdfs})

    except UserUploads.DoesNotExist as e:
        logging.error(f"UserUploads.DoesNotExist: {e}")
        return render(request, 'main/home.html', {'error_message': "Error Occurred"})
    

@login_required
def pdf_delete(request):

    if request.method == 'POST':
        user_pdfs = UserUploads.objects.filter(user=request.user)
        return render(request, 'user_profile.html', {'user_pdfs': user_pdfs})