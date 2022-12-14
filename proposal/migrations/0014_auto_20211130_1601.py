# Generated by Django 3.2.9 on 2021-11-30 16:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('proposal', '0013_alter_proposalmodel_submission_deadline'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposalsubmission',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='proposalsubmission',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='account.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='proposalsubmission',
            name='modified_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
