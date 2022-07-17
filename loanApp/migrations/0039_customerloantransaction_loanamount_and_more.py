# Generated by Django 4.0.2 on 2022-07-14 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loanApp', '0038_rename_payable_id_transaction_payment_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerloantransaction',
            name='loanAmount',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='customerloantransaction',
            name='payable_amount',
            field=models.FloatField(blank=True, max_length=20, null=True),
        ),
    ]
