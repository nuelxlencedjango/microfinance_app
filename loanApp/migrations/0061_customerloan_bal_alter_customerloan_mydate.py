# Generated by Django 4.0.2 on 2022-07-18 14:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loanApp', '0060_alter_customerloan_mydate'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerloan',
            name='bal',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='customerloan',
            name='mydate',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 19, 14, 44, 26, 558110)),
        ),
    ]
