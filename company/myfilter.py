import django_filters
from .models import *
from django import forms



class ApplicantsFilter(django_filters.FilterSet):
    min_age = django_filters.NumberFilter(field_name="sender__applicantprofile__birthday", lookup_expr='year__gt')
    max_age = django_filters.NumberFilter(field_name="sender__applicantprofile__birthday", lookup_expr='year__lt')
    position = django_filters.CharFilter(field_name='job__position', lookup_expr='icontains')
    class Meta:
        model = Applying
        fields= {'request':['exact'], 'experience':['exact'] }