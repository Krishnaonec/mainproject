from django.contrib import admin
from .models import CarBrand, CarModel, UserCar

@admin.register(CarBrand)
class CarBrandAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'display_total_models']

@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'carbrand', 'display_total_cars']

@admin.register(UserCar)
class UserCarAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'carbrand', 'carmodel', 'price', 'is_available']
    list_filter  = ['price', 'is_available']