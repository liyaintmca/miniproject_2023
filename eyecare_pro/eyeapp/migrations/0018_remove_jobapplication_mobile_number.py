# Generated by Django 4.2.4 on 2024-02-28 05:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eyeapp', '0017_jobapplication_job_designation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobapplication',
            name='mobile_number',
        ),
    ]
