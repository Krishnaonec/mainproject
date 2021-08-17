from django.contrib import admin
from .models import UserOwnerSpace, Webex

@admin.register(UserOwnerSpace)
class UserOwnerSpaceAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'roomId', 'creator', 'owner']
    

@admin.register(Webex)
class WebexAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'webex_id', 'webex_email', 'access_token']