# Generated by Django 4.0.2 on 2022-07-18 07:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loanApp', '0055_remove_loantransaction_amount_customerloan_mydate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerloan',
            name='mydate',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 19, 7, 3, 5, 467470)),
        ),
    ]
