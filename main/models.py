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
    is_deleted = models.BooleanField(default=False)
    deleted_at= models.DateTimeField(null=True, blank=True)


class Appointment(models.Model):
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_appointments')
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_appointments')
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='scheduled')
    reason = models.TextField(blank=True)
    comments = models.TextField(blank=True)
    duration = models.DurationField()