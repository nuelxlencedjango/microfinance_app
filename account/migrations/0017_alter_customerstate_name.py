# Generated by Django 4.0.2 on 2022-06-20 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0016_alter_customerstate_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerstate',
            name='name',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
    ]
