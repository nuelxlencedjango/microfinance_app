# Generated by Django 4.0.2 on 2022-07-18 07:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loanApp', '0057_alter_customerloan_mydate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customerloan',
            name='mydate',
        ),
    ]
