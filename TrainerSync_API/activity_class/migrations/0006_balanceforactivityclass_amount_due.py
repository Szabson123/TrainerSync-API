# Generated by Django 5.0.6 on 2024-06-11 13:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity_class', '0005_remove_balanceforactivityclass_amount_due_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='balanceforactivityclass',
            name='amount_due',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_have_to_pay', to='activity_class.activityclass'),
        ),
    ]