# Generated by Django 3.1.7 on 2021-05-06 09:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Forum', '0003_auto_20210505_1332'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appuser',
            name='keyLink',
        ),
        migrations.DeleteModel(
            name='ElasticDemo',
        ),
        migrations.RemoveField(
            model_name='questionsasked',
            name='keyLink',
        ),
        migrations.DeleteModel(
            name='AppUser',
        ),
        migrations.DeleteModel(
            name='QuestionsAsked',
        ),
        migrations.DeleteModel(
            name='UserCreds',
        ),
    ]
