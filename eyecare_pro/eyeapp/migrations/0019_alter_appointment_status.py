# Generated by Django 4.2.4 on 2023-10-05 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eyeapp', '0018_phar_reset_password_rep_reset_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]