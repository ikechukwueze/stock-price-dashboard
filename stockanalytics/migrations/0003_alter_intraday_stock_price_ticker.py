# Generated by Django 3.2.3 on 2021-06-01 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockanalytics', '0002_alter_eod_stock_price_ticker'),
    ]

    operations = [
        migrations.AlterField(
            model_name='intraday_stock_price',
            name='ticker',
            field=models.CharField(max_length=50),
        ),
    ]