# Generated by Django 4.2.3 on 2023-07-26 03:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_chat'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chat',
            old_name='received',
            new_name='recipient',
        ),
        migrations.RenameField(
            model_name='chat',
            old_name='send',
            new_name='sender',
        ),
    ]