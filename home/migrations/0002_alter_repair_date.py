# Generated by Django 5.1 on 2024-12-10 10:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repair',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 10, 10, 29, 39, 432079, tzinfo=datetime.timezone.utc)),
        ),
    ]