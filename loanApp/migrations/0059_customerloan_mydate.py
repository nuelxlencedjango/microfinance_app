# Generated by Django 4.0.2 on 2022-07-18 07:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loanApp', '0058_remove_customerloan_mydate'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerloan',
            name='mydate',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 19, 7, 29, 4, 679245)),
        ),
    ]
