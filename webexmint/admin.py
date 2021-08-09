from django.contrib import admin
from .models import UserOwnerSpace

@admin.register(UserOwnerSpace)
class UserOwnerSpaceAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'roomId', 'creator', 'owner']
    