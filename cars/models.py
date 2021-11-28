from django.db import models
from django.db.models.aggregates import Avg
from django.contrib.auth.models import User 
from rename_file import rename_car_pic
from image_utils import image_resize

class CarBrand(models.Model):
    name = models.CharField(max_length=50, unique = True)
    
    def __str__(self):
        return self.name
    
    def display_total_models(self):
        return self.carmodel_set.count()

    display_total_models.short_description = "Total no. of models available"


class CarModel(models.Model):
    name     = models.CharField(max_length=50, unique= True)
    carbrand = models.ForeignKey(CarBrand, on_delete= models.CASCADE)

    def __str__(self):
        return self.name
    
    def display_total_cars(self):
        return self.usercar_set.count()

    display_total_cars.short_description  = 'Total no. of cars '


class UserCar(models.Model):
    carbrand     = models.ForeignKey(CarBrand,verbose_name='Brand', on_delete= models.SET_NULL, null = True)
    carmodel     = models.ForeignKey(CarModel,verbose_name='Model', on_delete= models.SET_NULL, null = True)
    owner        = models.ForeignKey(User, on_delete= models.CASCADE)
    price        = models.DecimalField(verbose_name='price per day', max_digits=7, decimal_places=2)
    is_available = models.BooleanField(default= True)
    image        = models.ImageField(upload_to = rename_car_pic)

    def __str__(self):
        return f"{self.owner.username}'s {self.carmodel.name}"
    
    def get_rating(self):
        total_ratings = self.carbooking_set.count()
        if total_ratings:
            avg_rating = round(self.carbooking_set.aggregate(Avg('user_rating')), 1)
            return f"{(avg_rating['user_rating__avg'])}/5"
        else:
            return "No ratings"
        