from django.db import models
from django.contrib.auth.models import User
from rename_file import rename_profile_pic
from image_utils import image_resize

class Profile(models.Model):
    user  = models.OneToOneField(User, on_delete= models.CASCADE)
    # webex_email = models.EmailField(default= None, null= True)
    profile_pic = models.ImageField(upload_to = rename_profile_pic, default = "default_profile_pic.jpg")
    city = models.CharField(max_length=100,default="Hyderabad")
    owns_cars = models.BooleanField(default= False, null=True)

    def __str__(self):
        return self.user.username + " Profile"
    
    def save(self, *args, **kwargs):
        image_resize(self.profile_pic)
        super().save(*args, **kwargs)