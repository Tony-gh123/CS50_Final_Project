from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.db import models
from main.models import UserUploads, Chat
from django.http import HttpResponse
import logging
import os




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