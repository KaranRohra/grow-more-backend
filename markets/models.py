from django.db import models


class QuarterlyResult(models.Model):
    quarter = models.DateField()
    revenue = models.CharField(max_length=64)
    expenses = models.CharField(max_length=64)
    operating_profit = models.CharField(max_length=64)
    opm = models.CharField(max_length=64)
    other_income = models.CharField(max_length=64)
    interest = models.CharField(max_length=64)
    depreciation = models.CharField(max_length=64)
    profit_before_tax = models.CharField(max_length=64)
    tax = models.CharField(max_length=64)
    net_profit = models.CharField(max_length=64)
    eps_in_rs = models.CharField(max_length=64)
    symbol = models.CharField(max_length=64)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.stock}__{self.quarter}"
    
