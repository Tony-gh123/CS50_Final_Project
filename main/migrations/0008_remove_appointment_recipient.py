# Generated by Django 4.2.3 on 2023-08-03 10:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_appointment_recipient'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='recipient',
        ),
    ]
