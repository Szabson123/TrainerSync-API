# Generated by Django 5.0.6 on 2024-06-10 13:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0009_statute_room_alter_statute_owner'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='statute',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_name', to='rooms.room'),
        ),
        migrations.CreateModel(
            name='StatuteAcceptance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_accepted', models.BooleanField(default=False)),
                ('statute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='acceptances', to='rooms.statute')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_acceptnace', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
