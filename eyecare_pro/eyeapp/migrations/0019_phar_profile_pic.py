# Generated by Django 4.2.4 on 2024-03-04 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eyeapp', '0018_remove_jobapplication_mobile_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='phar',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics/'),
        ),
    ]
