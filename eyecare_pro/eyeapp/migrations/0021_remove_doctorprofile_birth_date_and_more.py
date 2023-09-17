# Generated by Django 4.2.4 on 2023-09-14 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eyeapp', '0020_docs_profile_pic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctorprofile',
            name='birth_date',
        ),
        migrations.RemoveField(
            model_name='doctorprofile',
            name='complete_date',
        ),
        migrations.RemoveField(
            model_name='doctorprofile',
            name='period_from',
        ),
        migrations.RemoveField(
            model_name='doctorprofile',
            name='period_to',
        ),
        migrations.RemoveField(
            model_name='doctorprofile',
            name='starting_date',
        ),
        migrations.AlterField(
            model_name='doctorprofile',
            name='gender',
            field=models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10, null=True),
        ),
    ]
