# Generated by Django 3.2.9 on 2021-11-25 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20211125_0857'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]