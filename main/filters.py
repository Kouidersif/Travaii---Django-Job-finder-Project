import django_filters
from .models import *
from django import forms
from django_filters import DateFilter



class SnippetFilter(django_filters.FilterSet):
    CHOICES = [
        ('ascending', 'Ascending'),
        ('descending', 'Descending')
    ]
    ordering = django_filters.ChoiceFilter(label='Ordering', choices = CHOICES, method = 'filter_by_order')
    min_price = django_filters.NumberFilter(field_name="salary_from", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="salary_to", lookup_expr='lte')

    
    class Meta:
        model = Jobs
        fields= {'job_category':['exact'],'work_from':['exact'],'job_type':['exact'],'job_shift':['exact'],'pay_per':['exact'],'interview_type':['exact'], 'creation_date': ['range'],
        'position':['exact', 'contains']}  

    def filter_by_order(self, queryset, name, value ):
        expression = 'creation_date' if value == 'ascending' else '-creation_date'
        return queryset.order_by(expression)
    @classmethod
    def filter_for_lookup(cls, f, lookup_type):
        # override date range lookups
        if isinstance(f, models.DateTimeField) and lookup_type == 'range':
            return django_filters.DateRangeFilter, {}

        # use default behavior otherwise
        return super().filter_for_lookup(f, lookup_type)
    