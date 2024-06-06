from django.contrib import admin
from .models import *


admin.site.register(Group)
admin.site.register(Room)
admin.site.register(InvitationCode)
admin.site.register(ActivityClass)