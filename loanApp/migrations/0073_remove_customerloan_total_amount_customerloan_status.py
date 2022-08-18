# Generated by Django 4.0.2 on 2022-07-22 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loanApp', '0072_customerloan_total_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customerloan',
            name='total_amount',
        ),
        migrations.AddField(
            model_name='customerloan',
            name='status',
            field=models.CharField(default='Not paid yet', max_length=20),
        ),
    ]