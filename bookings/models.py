from django.db import models
from django.contrib.auth.models import User
from cars.models import UserCar
from .validators import is_future_date

class CarBooking(models.Model):
    usercar        =  models.ForeignKey(UserCar, on_delete= models.SET_NULL , null=True)
    booked_user    =  models.ForeignKey(User, on_delete= models.SET_NULL, null = True)
    booked_date    =  models.DateField(auto_now_add=True)
    destination    = models.CharField(max_length=150,blank=True,null=True)
    returning_date = models.DateField(validators=[is_future_date])
    is_returned    = models.BooleanField(default=False)
    is_rated       = models.BooleanField(default=False)
    user_rating    = models.IntegerField(default=0)

    @property
    def booking_duration(self):
        return (self.returning_date - self.booked_date).days
    
    @property
    def bill_amount(self):
        bill = self.usercar.price * self.booking_duration
        return bill
    
    def __str__(self):
        return f"{self.booked_user.username}'s {self.usercar.carmodel.name}-{self.id}"