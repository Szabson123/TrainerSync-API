from django.db import models
from rooms.models import *
from users.models import *
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class ActivityClass(models.Model):
    name = models.CharField(max_length=255)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='activity_class_in_room')
    groups = models.ManyToManyField(Group, related_name='groups_in_activity_class', blank=True)
    users = models.ManyToManyField(CustomUser, related_name='users_in_activity_class', blank=True)
    subusers = models.ManyToManyField(SubUser, related_name='sub_users_in_activity_group', blank=True)
    cost = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    time = models.DurationField(null=True)
    
    def clean(self):
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError(_('End date cannot be earlier than start date'))
    
    def save(self, *args, **kwargs):
        if self.time and not self.end_date:
            self.end_date = self.start_date + self.time
        elif not self.time and self.end_date:
            self.time = self.end_date - self.start_date
        self.clean()
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.name


class BalanceForActivityClass(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='balance_user')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_in_balance')
    activity_class = models.ForeignKey(ActivityClass, on_delete=models.SET_NULL, null=True, related_name='activity_in_balance')
    amount_due = models.ForeignKey(ActivityClass, on_delete=models.SET_NULL, null=True, related_name='user_have_to_pay')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paid = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    
    def get_name(self):
        return self.activity_class.name if self.activity_class else "No Activity Class"

    def __str__(self):
        return f'{self.user} -- {self.get_name()}'