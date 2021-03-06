# Generated by Django 4.0.2 on 2022-07-14 20:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('loanApp', '0042_remove_loantransaction_amt_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerloan',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='loan_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='loantransaction',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transaction_customer', to=settings.AUTH_USER_MODEL),
        ),
    ]
