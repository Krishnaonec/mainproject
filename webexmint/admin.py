from django.contrib import admin
from .models import UserOwnerSpace, UserToken

@admin.register(UserOwnerSpace)
class UserOwnerSpaceAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'roomId', 'creator', 'owner']
    

@admin.register(UserToken)
class UserTokenAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'access_token']