# Generated by Django 4.0.5 on 2022-06-17 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_customersignup_ci_customersignup_nearest_bustop'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customersignup',
            old_name='city',
            new_name='state',
        ),
    ]
