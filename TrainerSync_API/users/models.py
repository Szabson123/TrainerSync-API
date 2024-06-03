from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_trainer = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    
    def __str__(self):
        return self.username

    REQUIRED_FIELDS = ['email']

    
class SubUser(models.Model):
    parent = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    number = models.CharField(max_length=15)
    
    def __str__(self) -> str:
        return f'Opiekun: {self.parent.get_full_name()} dziecko - {self.name} {self.last_name}'