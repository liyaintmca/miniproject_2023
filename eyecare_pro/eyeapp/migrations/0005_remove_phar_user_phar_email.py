# Generated by Django 4.2.4 on 2023-09-12 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eyeapp', '0004_doctorprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='phar',
            name='user',
        ),
        migrations.AddField(
            model_name='phar',
            name='email',
            field=models.EmailField(default='example@example.com', max_length=254),
        ),
    ]