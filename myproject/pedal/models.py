from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

# Create your models here.
# class AppUser(AbstractUser, PermissionsMixin):
#     #username=None
#     bits_id=models.CharField(unique=True,max_length=50)
#     profile_img    = models.ImageField(upload_to='images/Users/', null=True, blank=True, default=None)
#     # first_name = models.CharField(_("first_name"),max_length=50)
#     # last_name =  models.CharField(_("last_name"),max_length=50)
#     email = models.EmailField(_("email address"), unique=True)
#     phone = models.CharField(max_length=15)
#     address =  models.CharField(max_length=100)
    
#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = []
#     objects = CustomUserManager()
    

class AppUser(models.Model):
   #bits_id=models.CharField(unique=True,max_length=50)
   profile_img    = models.ImageField(upload_to='images/Users/', null=True, blank=True, default=None)
   #first_name = models.CharField(_("first_name"),max_length=50)
   #last_name =  models.CharField(_("last_name"),max_length=50)
   #email = models.EmailField(_("email address"), unique=True)
   address =  models.CharField(max_length=100)
   phone = models.CharField(max_length=15)
   authUser=models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

class Cycle(models.Model):
   cycle_img    = models.ImageField(null=True, blank=True, upload_to="images/")
   owner =models.ForeignKey(AppUser, blank=True, null=True, on_delete=models.SET_NULL)
   dop = models.DateTimeField('Date of Purchase')
   model = models.CharField(max_length=50)
   price=models.IntegerField()
   lend_or_sell = models.CharField(max_length=50)
   description = models.CharField(max_length=5000)
   is_avail=models.BooleanField(default=True)
   description = models.CharField(max_length=5000,null=True, blank=True)
   no_of_rents = models.IntegerField(default=0)
   total_stars=models.IntegerField(default=0)

   #Cycle(model='hero Razor back',address='1102 MSA 1 ',dop='06/09/19',price='190',img='cycle2.jpg')
   