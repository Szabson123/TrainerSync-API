# Generated by Django 5.0.6 on 2024-06-18 10:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0015_room_unaccepted_users'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='trainers',
            field=models.ManyToManyField(blank=True, null=True, related_name='trainer_in_room', to=settings.AUTH_USER_MODEL),
        ),
    ]