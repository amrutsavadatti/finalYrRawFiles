# Generated by Django 3.1.7 on 2021-05-15 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Forum', '0010_auto_20210515_0148'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='markSheet_verified',
            field=models.BooleanField(default=False),
        ),
    ]
