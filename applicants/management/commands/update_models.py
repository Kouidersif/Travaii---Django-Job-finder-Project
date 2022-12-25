from django.core.management.base import BaseCommand
import pandas as pd
from applicants.models import Cities,Wilaya, desired_Position
from main.models import Category





class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            'file_name', type=str, help='The txt file that contains the journal titles.')

    def handle(self, *args, **kwargs):
        file_name = kwargs['file_name']
        with open(f'{file_name}.txt') as file:
            for row in file:
                Wilaya.objects.create(
                    city_name = row
                )


