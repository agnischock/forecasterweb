# Generated by Django 2.0.1 on 2018-02-06 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forecaster', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forecast',
            name='gamma',
            field=models.FloatField(null=True),
        ),
    ]