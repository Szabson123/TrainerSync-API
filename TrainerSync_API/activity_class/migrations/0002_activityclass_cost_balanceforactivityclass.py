# Generated by Django 5.0.6 on 2024-06-11 10:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity_class', '0001_initial'),
        ('rooms', '0013_delete_activityclass'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='activityclass',
            name='cost',
            field=models.DecimalField(decimal_places=2, max_digits=6, null=True),
        ),
        migrations.CreateModel(
            name='BalanceForActivityClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_class', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='activity_in_balnce', to='activity_class.activityclass')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_in_balnce', to='rooms.room')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='balance_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
