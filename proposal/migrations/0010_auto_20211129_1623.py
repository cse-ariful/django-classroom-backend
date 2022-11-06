# Generated by Django 3.2.9 on 2021-11-29 16:23

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('proposal', '0009_auto_20211129_1611'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursemodel',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='account.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='coursemodel',
            name='code',
            field=models.CharField(max_length=50, unique=True, validators=[django.core.validators.RegexValidator(message='Invalid course Code', regex='(?i)[a-zA-Z]+-[0-9]+')]),
        ),
        migrations.AlterField(
            model_name='proposalmodel',
            name='submission_deadline',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 29, 16, 23, 46, 501455, tzinfo=utc)),
        ),
    ]