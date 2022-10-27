from django.db import models


class QuarterlyResult(models.Model):
    quarter = models.DateField()
    revenue = models.CharField()
    expenses = models.CharField()
    operating_profit = models.CharField()
    opm = models.CharField()
    other_income = models.CharField()
    interest = models.CharField()
    depreciation = models.CharField()
    profit_before_tax = models.CharField()
    tax = models.CharField()
    net_profit = models.CharField()
    eps_in_rs = models.CharField()
    symbol = models.CharField()
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.stock}__{self.quarter}"
    
