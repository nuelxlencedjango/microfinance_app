# Generated by Django 4.0.2 on 2022-07-14 04:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loanApp', '0015_alter_customerloan_customer_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='loanTransaction',
        ),
    ]
