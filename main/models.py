
from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.conf import settings
import datetime

now = timezone.now()

salary_range=[

        ('Per Year', 'Per Year'),
        ('Per Month', 'Per Month'),
        ('Per week', 'Per week'),
        ('Per Day', 'Per Day'),
        ('Per Hour', 'Per Hour'),
        ('Per Project', 'Per Project'),
    ]
interview=[
        ('Online', 'Online'),
        ('In Person', 'In Person'),
        ('Phone call', 'Phone call'),
    ]
Gender=[
    ('MALE','MALE'),
    ('FEMALE', 'FEMALE'),

]
SUBS=[
    ('Free', 'Free'),
    ('Gold', 'Gold'),
    ('Diamond', 'Diamond'),
]

class User(AbstractUser):
    full_name= models.CharField(max_length=25)
    is_company= models.BooleanField('is_company', default=False)
    is_applicant= models.BooleanField('is_applicant', default=False)
    phone_number= models.CharField(max_length=15,null=True, blank=True, unique=True)
    gender= models.CharField(max_length=10,choices=Gender)
    email= models.EmailField(unique=True)
    is_email_confirmed= models.BooleanField(default=False)
    source=models.ForeignKey('Where_socialMedia', on_delete=models.PROTECT, max_length=300,null=True, blank=True)
    registration_date= models.DateTimeField(auto_now_add=now)
    privacy_policy= models.BooleanField(default=True)







class Shifts(models.Model):
    shift= models.CharField(max_length=25, null=True, blank=True)
    def __str__(self):
        return self.shift

salary_cur=[
    ('€ Euro', '€ Euro '),
    ('$ USD', '$ USD'),
    ('£ EGP', '£ EGP'),

]

people_needd=[
    ('1-10', '1-10'),
    ('11-20', '11-20'),
    ('21-49', '21-49'),
    ('50-99', '50-99'),
    ('100-249', '100-249'),
    ('250-499', '250-499'),
    ('500-999', '500-999'),
    ('1000 or more', '1000 or more'),

]

class Jobs(models.Model):
    publisher= models.ForeignKey(User, related_name='work' ,on_delete=models.CASCADE, null=True) 
    job_category= models.ForeignKey('Category', related_name='myjobs' ,on_delete=models.SET_NULL, null=True)
    save_job= models.ManyToManyField(User, related_name='save_job', blank=True)
    position = models.CharField(max_length=200,null=True, blank=True)
    work_from= models.ForeignKey('Work_from', on_delete=models.SET_NULL,related_name='workplace', null=True, blank=True)
    job_type= models.ForeignKey('Job_type', on_delete=models.SET_NULL,related_name='typeofjob', null=True, blank=True)
    description = models.TextField()
    tasks= models.TextField(max_length=300,  null=True, blank=True)
    num_people= models.CharField(max_length=25,choices=people_needd, null=True, blank=True )
    is_urgent= models.BooleanField(default=False)
    job_shift=models.ForeignKey(Shifts,on_delete=models.SET_NULL, related_name='shifts', null=True, blank=True)
    salary_from = models.IntegerField(null=True, blank=True)
    salary_to = models.IntegerField(null=True, blank=True)
    salary_currency = models.CharField(max_length=15,choices=salary_cur, null=True)
    pay_per= models.CharField(max_length=150, null=True, blank=True, choices=salary_range)
    benifits= models.TextField(max_length=500, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=now)
    is_published= models.BooleanField(default=True)
    interview_type= models.CharField(max_length=50, choices=interview)

    def __str__(self):
        return self.position

class Category(models.Model):
    name= models.CharField(max_length=200, null=True, blank=True)
    image= models.ImageField(upload_to='category/bg/', null=True, blank=True)
    description= models.TextField(max_length=250, null=True, blank= True)
    def __str__(self):
        return self.name
    
    
class SearchedJobs(models.Model):
    search_content = models.CharField(max_length=500, null=True, blank=True)
    when = models.DateTimeField(auto_now_add=now)
    def __str__(self):
        return str(self.search_content) or 'Empty Search'
    

class Work_from(models.Model):
    work_from= models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return self.work_from

class Job_type(models.Model):
    job_type= models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return self.job_type

class Languages(models.Model):
    language= models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return self.language

class Skills(models.Model):
    owner= models.ForeignKey(User, on_delete=models.PROTECT)
    skill = models.CharField(max_length=200, null=True, blank=True)
    added = models.BooleanField(default=False)
    def __str__(self):
        return self.skill

class Where_socialMedia(models.Model):
    name=models.CharField(max_length=50, null=True, blank=True)
    def __str__(self):
        return self.name

class Education(models.Model):
    student= models.ForeignKey(User, on_delete=models.PROTECT)
    degree=models.CharField(max_length=200, null=True, blank=True)
    University= models.CharField(max_length=200, null=True, blank=True)
    speciality= models.CharField(max_length=200, null=True, blank=True)
    extra_info= models.TextField(null=True, blank=True)
    added = models.BooleanField(default=False)
    started= models.DateField()
    end= models.DateField(blank=True, null=True)
    submition_date= models.DateTimeField(auto_now_add=now)

    def __str__(self):
        return self.degree

stil = [
    ('Yes', 'Yes'),
    ('No', 'No'),
    
]

class Experience(models.Model):
    owner= models.ForeignKey(User, on_delete=models.PROTECT)
    title= models.CharField(max_length=200)
    company= models.CharField(max_length=150)
    company_pic_exp= models.ImageField(upload_to='experience/company/logo/', blank=True, null=True)
    co_location= models.CharField(max_length=300)
    started= models.DateField()
    end= models.DateField(blank=True, null=True)
    still_working= models.CharField(max_length=40,choices=stil)
    industry= models.CharField(max_length=100)
    about_role = models.TextField()
    added = models.BooleanField(default=False)
    submition_date= models.DateTimeField(auto_now_add=now)

    def __str__(self):
        return self.title




class Applying(models.Model):
    status=[
        ('Approved', 'Approved'),
        ('Pending', 'Pending'),
        ('Considered', 'Considered'),
        ('No Luck', 'No Luck'),
    ]
    exper=[
        ('Yes', 'Yes'),
        ('No','No'),
    ]
    job= models.ForeignKey(Jobs, on_delete=models.CASCADE)
    about= models.TextField(null=True, blank=True)
    sent_at= models.DateTimeField(auto_now_add=now)
    sender= models.ForeignKey(User, on_delete=models.CASCADE)
    expected_salary= models.CharField(max_length=10, null= True, blank=True)
    expected_salary_currency= models.CharField(max_length=15,choices=salary_cur, null=True, blank=True)
    experience= models.CharField(max_length=5, null=True, blank=True, choices=exper)
    request= models.CharField(max_length=10, choices=status, default='Pending' , null=True)
    response_message = models.TextField(null=True, blank=True)
    submited= models.BooleanField(default=False)



    def __str__(self):
        return self.job.position




@receiver(pre_save,sender=Applying)
def getNotified(sender, instance, **kwargs):
    try:
        old_instance = sender.objects.get(id=instance.id)
        mail_subject  = f'{instance.job.publisher.companyprofile.company_name} Replied to your application!'
        html_message  = f'Hello {instance.sender.full_name},<br><br> This is to inform you that {instance.job.publisher.companyprofile.company_name} has replied to your application for {instance.job.position} position. We encourage you to log in to your account and check the response.<br><br>'
        html_message += 'Best regards,<br>The Travaii Team'
        from_email='support@travaii.com'
        message = EmailMessage(mail_subject, html_message,from_email, to=[instance.sender.email])
        message.content_subtype = 'html' # this is required because there is no plain text email version
        if old_instance.request != instance.request or old_instance.response_message != instance.response_message :
            message.send()
    except sender.DoesNotExist:
        # This means the instance is being created for the first time,
        print('no')
        


class ContactUs(models.Model):
    full_name= models.CharField(max_length=100)
    email= models.EmailField()
    title=models.CharField(max_length=300)
    message= models.TextField(max_length=5000)
    sent_at= models.DateTimeField(auto_now_add=now)


    def __str__(self):
        return self.title



class Get_industry(models.Model):
    industry_name = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return self.industry_name




class number_user_facebook(models.Model):
    users_l = models.IntegerField(default=0, null=True, blank=True)
    def __str__(self):
        return f'Total visits from facebook : {self.users_l}'