# Generated by Django 4.2.4 on 2023-09-13 18:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eyeapp', '0017_alter_customuser_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='docs',
            name='role',
        ),
        migrations.AddField(
            model_name='docs',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, ' PATIENTS'), (2, 'DOCTORS'), (3, 'RECEPIONISTS'), (4, 'PHARMACISTS'), (5, 'ADMIN')], default='1', null=True),
        ),
    ]