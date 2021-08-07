from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from cars.models import UserCar

@receiver(post_save, sender = UserCar)
def update_owner_status(sender, instance, created, *args, **kwargs):
    if created:
        user = User.objects.filter(username = instance.owner.username).first()
        user.profile.owns_cars = True 
        user.save()

@receiver(post_delete, sender = UserCar)
def remove_ownership(sender, instance, *args, **kwargs):
    user = User.objects.filter(username = instance.owner.username).first()
    if user.usercar_set.count() == 0:
        user.profile.owns_cars = False
        user.save()
    else:
        pass 