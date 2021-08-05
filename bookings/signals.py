from django.dispatch import receiver
from django.db.models.signals import post_save
from cars.models import UserCar
from bookings.models import CarBooking

@receiver(post_save, sender = CarBooking)
def update_car_availability(sender, instance, created, *args, **kwargs):
    if created:
        usercar = UserCar.objects.filter(id = instance.usercar.id).first()
        usercar.is_available = False
        usercar.save()