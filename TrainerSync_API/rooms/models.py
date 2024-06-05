from django.db import models
from users.models import CustomUser
import uuid    
    
    
class Room(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='owned_rooms')
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    
    def generate_code(self):
        code = uuid.uuid4().hex[:6].upper()
        while InvitationCode.objects.filter(code=code).exists():
            InvitationCode.objects.create(room=self, code=code)
        return code
    
    def __str__(self) -> str:
        return self.name
    

class InvitationCode(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    
    def __str__(self) -> str:
        return self.code 


class Group(models.Model):
    name = models.CharField(max_length=255)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='groups_in_room')
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.name