# Generated by Django 4.0.2 on 2022-07-14 20:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loanApp', '0039_customerloantransaction_loanamount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='loanApp.customerloan'),
        ),
    ]
