# Generated by Django 4.0.2 on 2022-07-14 07:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loanApp', '0020_remove_loantransaction_amt'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loantransaction',
            name='transaction',
        ),
    ]
