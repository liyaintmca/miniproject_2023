# Generated by Django 4.2.4 on 2024-02-28 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eyeapp', '0014_alter_careeropening_experience_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='careeropening',
            name='vacancies',
            field=models.PositiveIntegerField(blank=True, default=1, null=True),
        ),
    ]
