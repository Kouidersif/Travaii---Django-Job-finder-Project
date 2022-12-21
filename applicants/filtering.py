import django_filters
from .models import *
from django import forms



class CandidateFilter(django_filters.FilterSet):
    #year_joined = django_filters.NumberFilter(field_name='birthday', lookup_expr='year')
    year_joined__gt = django_filters.NumberFilter(field_name='birthday', lookup_expr='year__gt')
    year_joined__lt = django_filters.NumberFilter(field_name='birthday', lookup_expr='year__lt')


    class Meta:
        model = ApplicantProfile
        fields={'languages':['exact'], 'desired_industry':['exact'],
        'state':['exact'], 'desired_job':['exact'], 'desired_job_type':['exact'], 'desired_shift':['exact'],
        #'birthday':['year', 'year__gt', 'year__lt', ],
      
        }
    @classmethod
    def filter_for_lookup(cls, f, lookup_type):
        # override date range lookups
        if isinstance(f, models.DateTimeField) and lookup_type == 'range':
            return django_filters.DateRangeFilter, {}

        # use default behavior otherwise
        return super().filter_for_lookup(f, lookup_type)



