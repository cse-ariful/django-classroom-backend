# Generated by Django 3.2.9 on 2021-11-29 16:25

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('proposal', '0010_auto_20211129_1623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposalmodel',
            name='submission_deadline',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 29, 16, 25, 52, 955804, tzinfo=utc)),
        ),
    ]
