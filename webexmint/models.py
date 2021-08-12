from django.db import models
from django.contrib.auth.models import User

class UserOwnerSpace(models.Model):
    creator = models.ForeignKey(User, on_delete= models.CASCADE)
    title   = models.CharField(max_length=200, unique= True)
    roomId  = models.TextField()
    owner   = models.ForeignKey(User, on_delete= models.CASCADE, related_name='owner')
    def __str__(self):
        return self.title

class UserToken(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    access_token = models.TextField(null= True, default= None)