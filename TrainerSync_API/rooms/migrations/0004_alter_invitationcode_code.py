# Generated by Django 5.0.6 on 2024-06-06 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0003_group_subusers_group_users_room_subusers_room_users_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitationcode',
            name='code',
            field=models.CharField(max_length=6, unique=True),
        ),
    ]