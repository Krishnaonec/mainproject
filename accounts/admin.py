from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','city', 'id']
    list_filter  = ['city', 'owns_cars']