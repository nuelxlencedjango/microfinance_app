# Generated by Django 4.0.2 on 2022-07-15 06:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loanApp', '0050_alter_loantransaction_transaction_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loantransaction',
            name='payment_id',
        ),
        migrations.RemoveField(
            model_name='loantransaction',
            name='transaction_id',
        ),
    ]
