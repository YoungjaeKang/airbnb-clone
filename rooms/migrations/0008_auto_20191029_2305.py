# Generated by Django 2.2.5 on 2019-10-29 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0007_auto_20191028_2215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='file',
            field=models.ImageField(upload_to='room_photos'),
        ),
    ]
