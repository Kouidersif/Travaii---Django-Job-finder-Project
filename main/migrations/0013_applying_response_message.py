# Generated by Django 4.1.3 on 2023-02-06 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_alter_jobs_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='applying',
            name='response_message',
            field=models.TextField(blank=True, null=True),
        ),
    ]