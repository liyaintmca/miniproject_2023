# Generated by Django 4.2.4 on 2024-02-28 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eyeapp', '0013_careeropening'),
    ]

    operations = [
        migrations.AlterField(
            model_name='careeropening',
            name='experience',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='careeropening',
            name='job_designation',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='careeropening',
            name='qualifications',
            field=models.TextField(blank=True, null=True),
        ),
    ]
