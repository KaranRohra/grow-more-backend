# Generated by Django 4.1.1 on 2022-10-26 09:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Stock",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("company_name", models.CharField(max_length=256)),
                ("industry", models.CharField(max_length=256)),
                ("nse_symbol", models.CharField(max_length=256, unique=True)),
                ("bse_symbol", models.CharField(max_length=256, unique=True)),
                ("yahoo_symbol", models.CharField(max_length=256, unique=True)),
                ("isin_code", models.CharField(max_length=256, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="ShareHoldingPattern",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quarter", models.CharField(max_length=32)),
                ("promoter", models.CharField(max_length=3)),
                ("fiis", models.CharField(max_length=3)),
                ("diis", models.CharField(max_length=3)),
                ("public", models.CharField(max_length=3)),
                ("government", models.CharField(max_length=3)),
                ("other", models.CharField(max_length=3)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "stock",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="markets.stock"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Cashflow",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("year", models.CharField(max_length=32)),
                ("cash_from_operating_activity", models.CharField(max_length=128)),
                ("cash_from_investing_activity", models.CharField(max_length=128)),
                ("cash_from_financing_activity", models.CharField(max_length=128)),
                ("net_cash_flow", models.CharField(max_length=128)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "stock",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="markets.stock"
                    ),
                ),
            ],
        ),
    ]
