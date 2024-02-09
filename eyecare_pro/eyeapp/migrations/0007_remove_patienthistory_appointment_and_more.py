# Generated by Django 4.2.4 on 2024-02-08 05:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eyeapp', '0006_remove_prescription_dosage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patienthistory',
            name='Appointment',
        ),
        migrations.AddField(
            model_name='patienthistory',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
