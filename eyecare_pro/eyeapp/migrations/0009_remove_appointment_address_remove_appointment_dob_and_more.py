# Generated by Django 4.2.4 on 2024-02-08 10:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eyeapp', '0008_patienthistory_address_patienthistory_dob_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='address',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='dob',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='mobile',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='name',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='place',
        ),
        migrations.AddField(
            model_name='appointment',
            name='patientHistory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='patient_history', to='eyeapp.patienthistory'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='allergy',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='doctor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='eyeapp.docs'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='reason',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
