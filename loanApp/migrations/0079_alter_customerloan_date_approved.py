# Generated by Django 4.0.2 on 2022-07-24 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loanApp', '0078_remove_customerbank_bvn_remove_customerbank_nin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerloan',
            name='date_approved',
            field=models.DateField(auto_now=True),
        ),
    ]