# Generated by Django 5.0.6 on 2024-06-18 10:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0014_room_description'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='unaccepted_users',
            field=models.ManyToManyField(related_name='unaccepted_users', to=settings.AUTH_USER_MODEL),
        ),
    ]
