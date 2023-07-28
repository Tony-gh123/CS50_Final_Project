from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserUploads(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pdf_file = models.FileField(upload_to='pdf_files/', blank=True, null=True)


class Chat(models.Model):
    
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received')
    content = models.TextField()
    file = models.FileField(upload_to='chat_files/%Y/%m/%d/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)



