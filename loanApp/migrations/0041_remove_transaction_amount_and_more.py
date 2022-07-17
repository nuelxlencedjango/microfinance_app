# Generated by Django 4.0.2 on 2022-07-14 20:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('loanApp', '0040_alter_transaction_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='loantransaction',
            name='am',
        ),
        migrations.AlterField(
            model_name='customerbank',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='customer_bank', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='customerloan',
            name='customer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='loan_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='customerloan',
            name='payable_loan',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='customerloan',
            name='total_loan',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='loanrequest',
            name='customer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='customer_loan', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='loantransaction',
            name='customer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='transaction_customer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='repayment',
            name='customer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='loan_repayment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='CustomerLoanTransaction',
        ),
        migrations.DeleteModel(
            name='Transaction',
        ),
    ]
