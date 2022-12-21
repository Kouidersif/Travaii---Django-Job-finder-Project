# Generated by Django 4.1.3 on 2022-12-19 23:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicants', '0006_rename_reason_delete_account_feedback_reason_txt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicantprofile',
            name='applicant_cv',
            field=models.FileField(blank=True, upload_to='resume/applicant/%y/%m/%d', validators=[django.core.validators.FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])]),
        ),
    ]
