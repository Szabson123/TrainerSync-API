from django.db import models
from users.models import CustomUser, SubUser
import uuid    
    
    
class Room(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='owned_rooms')
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    trainers = models.ManyToManyField(CustomUser, related_name='trainer_in_room')
    users = models.ManyToManyField(CustomUser, related_name='users_in_room')
    subusers = models.ManyToManyField(SubUser, related_name='sub_users_in_room')
    
    def generate_code(self):
        code = uuid.uuid4().hex[:6].upper()
        while InvitationCode.objects.filter(code=code).exists():
            code = uuid.uuid4().hex[:6].upper()
            InvitationCode.objects.create(room=self, code=code)
        return code
    
    def __str__(self) -> str:
        return self.name
    

class InvitationCode(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, unique=True)
    
    def __str__(self) -> str:
        return self.code 


class Group(models.Model):
    name = models.CharField(max_length=255)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='groups_in_room')
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(CustomUser, related_name='users_in_group', blank=True)
    subusers = models.ManyToManyField(SubUser, related_name='sub_users_in_group', blank=True)
    
    def __str__(self) -> str:
        return self.name
    

class ActivityClass(models.Model):
    name = models.CharField(max_length=255)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='activity_class_in_room')
    groups = models.ManyToManyField(Group, related_name='groups_in_activity_class', blank=True)
    users = models.ManyToManyField(CustomUser, related_name='users_in_activity_class', blank=True)
    subusers = models.ManyToManyField(SubUser, related_name='sub_users_in_activity_group', blank=True)
    
    def __str__(self) -> str:
        return self.name
    
    
class Statute(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_name')
    description = models.TextField()
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='statue_owner')