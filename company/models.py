from django.db import models
import datetime
from main.models import *
# Create your models here.
from applicants.models import Wilaya, Cities
from django.core.exceptions import ValidationError
now = datetime

company_size=[
    ('1-10', '1-10'),
    ('11-20', '1-20'),
    ('21-49', '21-49'),
    ('50-99', '50-99'),
    ('100-249', '100-249'),
    ('250-499', '250-499'),
    ('500-999', '500-999'),
    ('1000 or more', '1000 or more'),

]

class CompanyProfile(models.Model):
    owner= models.OneToOneField(User, on_delete=models.CASCADE ) 
    followers= models.ManyToManyField(User, related_name='user_followers', blank=True)
    website=models.URLField(max_length=100, null=True, blank=True, unique=True)
    facebook= models.URLField(max_length=100, null=True, blank=True, unique=True)
    twitter= models.URLField(max_length=100, null=True, blank=True, unique=True)
    github= models.URLField(max_length=100, null=True, blank=True, unique=True)
    address= models.CharField(max_length=100, null=True, blank=True)
    about= models.TextField()
    city= models.ForeignKey(Cities, related_name='company_city', on_delete=models.SET_NULL, null=True, blank=False)
    state= models.ForeignKey(Wilaya, related_name='company_wilaya', on_delete=models.SET_NULL, null=True, blank=False)
    zip_code= models.IntegerField(default=0)
    company_logo=models.ImageField(null=True, blank=True, upload_to='company/%y/%m/%d')
    profile_bg= models.ImageField(null=True, blank=True, upload_to='company/bg/%y/%m/%d')
    founded= models.CharField(max_length=15, null=False, blank=False)
    co_size= models.CharField(max_length=50,choices=company_size, null=False, blank=False)
    industry= models.CharField(max_length=40)
    company_name= models.CharField(max_length=30, unique=True)
    is_profile_completed= models.BooleanField(default=False)
    submition_date= models.DateTimeField(auto_now_add=now)
    instagram=models.URLField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return self.company_name

    
    

class Photos_c(models.Model):
    photo_publisher = models.ForeignKey(User, on_delete=models.PROTECT, null=True, related_name='photo_owner')
    tag = models.CharField(max_length=500, null=True, blank=True)
    the_images= models.ImageField(upload_to='company/photos/%y/%m/%d')
    is_public= models.BooleanField(default=True)
    published_on= models.DateTimeField(auto_now_add=now)
    def __str__(self):
        return self.photo_publisher.companyprofile.company_name





