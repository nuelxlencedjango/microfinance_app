# Generated by Django 4.0.2 on 2022-07-23 12:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loanApp', '0077_delete_repayment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customerbank',
            name='bvn',
        ),
        migrations.RemoveField(
            model_name='customerbank',
            name='nin',
        ),
    ]