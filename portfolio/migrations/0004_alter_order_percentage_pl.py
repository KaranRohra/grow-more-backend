# Generated by Django 4.1.3 on 2023-01-05 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0003_order_percentage_pl_order_profit_loss"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="percentage_pl",
            field=models.FloatField(default=0),
        ),
    ]
