# Generated by Django 4.0.2 on 2022-07-15 06:08

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('loanApp', '0048_alter_loantransaction_transaction_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loantransaction',
            name='transaction_id',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=36),
        ),
    ]
