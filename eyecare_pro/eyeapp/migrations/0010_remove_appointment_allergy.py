# Generated by Django 4.2.4 on 2024-02-09 09:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eyeapp', '0009_remove_appointment_address_remove_appointment_dob_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='allergy',
        ),
    ]