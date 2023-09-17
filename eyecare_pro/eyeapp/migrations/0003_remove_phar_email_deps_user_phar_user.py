# Generated by Django 4.2.4 on 2023-09-12 01:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eyeapp', '0002_remove_docs_email_docs_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='phar',
            name='email',
        ),
        migrations.AddField(
            model_name='deps',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='phar',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]