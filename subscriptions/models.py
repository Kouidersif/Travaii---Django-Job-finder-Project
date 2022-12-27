from django.db import models
from main.models import User


import datetime

dat = datetime.date.today


Prices=[
    ('Year','Year'),
    ('Month', 'Month'),
]
subsc=[
    ('Free', 'Free'),
    ('Large enterprise', 'Large enterprise'),
    ('Mid-market enterprises', 'Mid-market enterprises'),
    ('Small business', 'Small business'),
    ('Trialing', 'Trialing'),
]
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripeid = models.CharField(max_length=255)
    stripe_subscription_id = models.CharField(max_length=255)
    cancel_at_period_end = models.BooleanField(default=False)
    membership = models.BooleanField(default=False)
    selected_membership= models.CharField(max_length=150, choices=subsc, null=True)
    track_id= models.CharField(max_length=20,null=True, unique=True)
    created_at= models.DateTimeField(auto_now_add=dat)

    def __str__(self):
        return self.user.username
    

class ProName(models.Model):
    created_by=models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    product_ids= models.CharField(max_length=150)
    price_per_year = models.IntegerField()
    price_year_id_code= models.CharField(max_length=150)
    #year_description= models.CharField(max_length=200)
    ####
    price_per_month= models.IntegerField()
    price_month_id_code= models.CharField(max_length=150)
    #month_description= models.CharField(max_length=200)
    #######
    created_at= models.DateTimeField(auto_now_add=dat)

    

    def __str__(self):
        return self.name

class Features(models.Model):
    offer = models.OneToOneField(ProName,on_delete=models.CASCADE, related_name='feat')
    feature= models.CharField(max_length=200)
    def __str__(self):
        return self.offer.name