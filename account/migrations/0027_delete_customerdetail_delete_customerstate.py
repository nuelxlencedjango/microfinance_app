# Generated by Django 4.0.2 on 2022-06-21 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loanApp', '0002_alter_customerbank_customer_and_more'),
        ('account', '0026_remove_customerdetail_state_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomerDetail',
        ),
        migrations.DeleteModel(
            name='CustomerState',
        ),
    ]
