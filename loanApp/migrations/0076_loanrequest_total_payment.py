# Generated by Django 4.0.2 on 2022-07-23 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loanApp', '0075_alter_customerloan_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanrequest',
            name='total_payment',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
