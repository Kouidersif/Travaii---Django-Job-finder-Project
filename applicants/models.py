from django.db import models
from main.models import *
import datetime
from datetime import date
now = datetime
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model



User = get_user_model()



# Create your models here.


class desired_Position(models.Model):
    name = models.CharField(max_length=250)
    def __str__(self):
        return self.name

class Cities(models.Model):
    city_name=models.CharField(max_length=300)
    def __str__(self):
        return self.city_name


class Wilaya(models.Model):
    city_name=models.CharField(max_length=300)
    def __str__(self):
        return self.city_name

class ApplicantProfile(models.Model):
    degrees=[
        ('Associate', 'Associate'),
        ("Bachelor's", "Bachelor's"),
        ("Master's", "Master's"),
        ('Doctoral', 'Doctoral'),
    ]
    lenguas=[
        ('french', 'french'),
        ('arabic', 'arabic'),
        ('spanish', 'spanish')
    ]
    privacy=[
        ('Anyone','Anyone'),
        ('Only you','Only you'),
    ]
    owner= models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic= models.ImageField(blank=True)
    city= models.ForeignKey(Cities, related_name='applicant_city', on_delete=models.SET_NULL, null=True)
    state= models.ForeignKey(Wilaya, related_name='applicant_wilaya', on_delete=models.SET_NULL, null=True)
    languages= models.ManyToManyField(Languages,blank=True)
    linkedin= models.URLField(blank=True, null=True, unique=True)
    save_applicant= models.ManyToManyField(User, related_name='save_applicant', blank=True)
    github= models.URLField(blank=True, null=True, unique=True)
    p_website= models.URLField(blank=True, null=True, unique=True)
    desired_job= models.ForeignKey(desired_Position, related_name='applicant_job',blank=True, on_delete=models.SET_NULL, null=True)
    desired_industry= models.ForeignKey(Category, on_delete=models.SET_NULL, null=True,blank=True, related_name='applicant_job_industry')
    desired_job_type= models.ForeignKey(Job_type, on_delete=models.SET_NULL, related_name='applicant_job_type', null=True,blank=True)
    desired_shift= models.ForeignKey(Shifts,on_delete=models.SET_NULL, null=True,related_name='applicant_job_shift', blank=True)
    applicant_cv= models.FileField(blank=True, upload_to='resume/applicant/%y/%m/%d',
    validators=[FileExtensionValidator( ['pdf', 'jpg', 'jpeg', 'png', 'docx'] ) ]
    )
    birthday= models.DateField(null=True)
    about= models.TextField(null=True, blank=True)
    is_public= models.CharField(max_length=20, choices=privacy, default='Anyone')
    facebook= models.URLField(blank=True, null=True)
    instagram= models.URLField(blank=True, null=True)
    submited = models.BooleanField(default=False)
    submition_date= models.DateTimeField(auto_now_add=now)
    def __str__(self):
        return self.owner.username

    @property
    def calculate_age(self):
        today = date.today()
        calcu =  today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
        return calcu

reasons=[
    ("I don't understand how to use Travaii", "I don't understand how to use Travaii"), 
    ("I don't find Travaii useful", "I don't find Travaii useful"), 
    ("I'm getting too many spam calls and emails","I'm getting too many spam calls and emails"),
    ("I have privacy concerns","I have privacy concerns"),
]
class Delete_account_Feedback(models.Model):
    the_reason = models.CharField(choices=reasons, max_length=300, blank=True, null=True)
    reason_txt = models.TextField()
    email_user= models.CharField(max_length=300, blank=True, null=True)
    def __str__(self):
        return self.the_reason or 'feedback'




class NewsLetter(models.Model):
    email_field = models.EmailField()
    job_category = models.CharField(max_length=300, null=True, blank = True)
    def __str__(self):
        return str(self.job_category) or (self.email_field) or ''
    


@receiver(signal=post_save, sender=User)
def create_applicant_profile(instance, created,  **kwargs):

    if created and instance.is_applicant == True:
        
        user = User.objects.get(id=instance.id)
        ApplicantProfile.objects.create(owner = user)

