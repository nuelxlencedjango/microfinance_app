# Generated by Django 4.0.2 on 2022-07-15 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loanApp', '0053_alter_loanrequest_days'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loanrequest',
            name='days',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
