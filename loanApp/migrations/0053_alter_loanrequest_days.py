# Generated by Django 4.0.2 on 2022-07-15 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loanApp', '0052_rename_transaction_loantransaction_transaction_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loanrequest',
            name='days',
            field=models.IntegerField(default=1),
        ),
    ]
