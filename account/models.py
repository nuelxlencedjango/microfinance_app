from unicodedata import name
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
#from django.db.models.signals import post_save
from django.dispatch import receiver
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser

#from django.contrib.auth import get_user_model

#User = get_user_model()



class State(models.Model):
    name = models.CharField(max_length=50,null=True,unique=True)
    def __str__(self):

        return self.name




class Location(models.Model):
    area = models.CharField(max_length=50,null=True)

    def __str__(self):
        return self.area




class CustomerInfo(models.Model):
    user = models.OneToOneField(User,null=True,blank=True, on_delete= models.SET_NULL,related_name='customer_info')

    address = models.CharField(max_length=50,null=True)
    nearest_bustop = models.CharField(max_length=50,null=True)
    location =  models.ForeignKey(Location, on_delete=models.CASCADE,null=True,blank=True)
    business = models.CharField(max_length=50,null=True)
    profile_img = CloudinaryField(blank=True,null=True)
    phone = models.CharField(max_length=11,null=True,unique=True) 
    state = models.ForeignKey(State, on_delete=models.CASCADE,null=True,blank=True)
    dateRegistered =models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.user)



   
        
        


