# Generated by Django 5.0.6 on 2024-06-10 13:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0008_room_trainers'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='statute',
            name='room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='room_name', to='rooms.room'),
        ),
        migrations.AlterField(
            model_name='statute',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statue_owner', to=settings.AUTH_USER_MODEL),
        ),
    ]