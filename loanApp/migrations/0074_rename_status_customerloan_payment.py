# Generated by Django 4.0.2 on 2022-07-22 22:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loanApp', '0073_remove_customerloan_total_amount_customerloan_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customerloan',
            old_name='status',
            new_name='payment',
        ),
    ]
