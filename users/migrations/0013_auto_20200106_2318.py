# Generated by Django 2.2.5 on 2020-01-06 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20200106_2308'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='eamil_secret',
        ),
        migrations.AddField(
            model_name='user',
            name='email_secret',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
    ]
