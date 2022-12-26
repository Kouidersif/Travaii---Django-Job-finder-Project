# Generated by Django 4.1.3 on 2022-12-26 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_education_end_alter_experience_end'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobs',
            name='salary',
        ),
        migrations.AddField(
            model_name='jobs',
            name='salary_from',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='jobs',
            name='salary_to',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='full_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='title',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='education',
            name='University',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='education',
            name='degree',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='education',
            name='speciality',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='experience',
            name='co_location',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='experience',
            name='company',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='experience',
            name='title',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='job_type',
            name='job_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='languages',
            name='language',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='skills',
            name='skill',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='where_socialmedia',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='work_from',
            name='work_from',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
