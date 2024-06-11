from django.db import models



class ActivityClass(models.Model):
    name = models.CharField(max_length=255)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='activity_class_in_room')
    groups = models.ManyToManyField(Group, related_name='groups_in_activity_class', blank=True)
    users = models.ManyToManyField(CustomUser, related_name='users_in_activity_class', blank=True)
    subusers = models.ManyToManyField(SubUser, related_name='sub_users_in_activity_group', blank=True)
    
    def __str__(self) -> str:
        return self.name
