from django.db import models


class Stock(models.Model):
    name = models.CharField(max_length=20)
    symbol = models.CharField(max_length=20)


class ProfitAndLoss(models.Model):
    symbol = models.ForeignKey(Stock, on_delete=models.CASCADE)
    year = models.CharField(max_length=20)
    revenue = models.CharField(max_length=20)
    expenses = models.CharField(max_length=20)
    operating_profit = models.CharField(max_length=20)
    opm = models.CharField(max_length=20)
    other_income = models.CharField(max_length=20)
    interest = models.CharField(max_length=20)
    depreciation = models.CharField(max_length=20)
    profit_before_tax = models.CharField(max_length=20)
    tax = models.CharField(max_length=20)
    net_profit = models.CharField(max_length=20)
    eps = models.CharField(max_length=20)
    dividend_payout = models.CharField(max_length=20,blank=True,null=True)
