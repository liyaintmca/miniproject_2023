# Generated by Django 4.2.4 on 2023-10-01 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eyeapp', '0015_medicine'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicine',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='medicinecategory',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
