# Generated by Django 4.0.2 on 2022-07-14 12:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loanApp', '0025_loantransaction_amt_loantransaction_transaction_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loantransaction',
            name='amt',
        ),
    ]
