# Generated by Django 5.1.4 on 2025-02-03 16:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_repair_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repair',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2025, 2, 3, 16, 50, 54, 756644, tzinfo=datetime.timezone.utc)),
        ),
    ]
