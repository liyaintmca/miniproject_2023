# Generated by Django 4.2.4 on 2024-02-28 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eyeapp', '0012_leave'),
    ]

    operations = [
        migrations.CreateModel(
            name='CareerOpening',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_designation', models.CharField(max_length=100)),
                ('qualifications', models.TextField()),
                ('experience', models.CharField(max_length=50)),
            ],
        ),
    ]