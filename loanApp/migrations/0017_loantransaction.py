# Generated by Django 4.0.2 on 2022-07-14 04:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('loanApp', '0016_delete_loantransaction'),
    ]

    operations = [
        migrations.CreateModel(
            name='loanTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction', models.UUIDField(default=uuid.uuid4, editable=False, null=True)),
                ('transaction_id', models.CharField(default=uuid.uuid4, editable=False, max_length=10)),
                ('payment', models.PositiveIntegerField(default=0)),
                ('payment_date', models.DateField(auto_now_add=True)),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='transaction_customer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
