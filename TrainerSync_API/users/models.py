from django.contrib.auth.models import AbstractUser
from django.db import models
from rooms.models import Room, Group

class CustomUser(AbstractUser):
    is_trainer = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    room = models.ManyToManyField(Room, related_name='user_in_rooms', blank=True)
    groups = models.ManyToManyField(Group, related_name='user_in_group', blank=True)
    
    
    
    def __str__(self):
        return self.username

    REQUIRED_FIELDS = ['email']

    
class SubUser(models.Model):
    parent = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    number = models.CharField(max_length=15)
    room = models.ManyToManyField(Room, related_name='sub_user_in_rooms', blank=True)
    groups = models.ManyToManyField(Group, related_name='sub_user_in_group', blank=True)
    
    def __str__(self) -> str:
        return f'Opiekun: {self.parent.get_full_name()} dziecko - {self.name} {self.last_name}'