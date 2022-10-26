from django.db import models


class ProfitAndLoss(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    year = models.CharField(max_length=32)
    revenue = models.CharField(max_length=128)
    expenses = models.CharField(max_length=128)
    operating_profit = models.CharField(max_length=128)
    opm = models.CharField(max_length=128)
    other_income = models.CharField(max_length=128)
    interest = models.CharField(max_length=128)
    depreciation = models.CharField(max_length=128)
    profit_before_tax = models.CharField(max_length=128)
    tax = models.CharField(max_length=128)
    net_profit = models.CharField(max_length=128)
    eps_in_rs = models.CharField(max_length=128)
    dividend_payout = models.CharField(max_length=128, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
