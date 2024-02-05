# Generated by Django 4.2.4 on 2024-02-01 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eyeapp', '0002_blog_extended_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicine',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='medicine',
            name='details',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='medicine',
            name='expiryDate',
            field=models.DateField(blank=True, null=True),
        ),
    ]
