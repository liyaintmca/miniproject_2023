# Generated by Django 4.2.4 on 2024-03-15 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eyeapp', '0021_donation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('photo', models.ImageField(upload_to='awards/photos/')),
            ],
        ),
    ]
