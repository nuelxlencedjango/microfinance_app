# Generated by Django 4.0.2 on 2022-07-14 17:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loanApp', '0036_alter_transaction_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='amount',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='loanApp.customerloan'),
        ),
    ]
