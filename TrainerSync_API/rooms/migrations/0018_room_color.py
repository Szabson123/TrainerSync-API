# Generated by Django 5.0.6 on 2024-08-20 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0017_alter_room_subusers_alter_room_unaccepted_users_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='color',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]