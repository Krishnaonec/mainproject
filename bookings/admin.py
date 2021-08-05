from django.contrib import admin
from .models import CarBooking

@admin.register(CarBooking)
class CarBookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'booked_user', 'usercar', 'booked_date', 'returning_date', 'bill_amount', 'is_returned')
    list_filter  = ('is_returned',)