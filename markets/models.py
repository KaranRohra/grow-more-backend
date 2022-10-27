from django.db import models


class BalanceSheet(models.Model):
    year = models.CharField(max_length=32)
    share_capital = models.CharField(max_length=64)
    reserves = models.CharField(max_length=64)
    borrowings = models.CharField(max_length=64)
    other_liabilities = models.CharField(max_length=64)
    total_liabilities = models.CharField(max_length=64)
    fixed_assets = models.CharField(max_length=64)
    cwip = models.CharField(max_length=64)
    investmments = models.CharField(max_length=64)
    other_assets = models.CharField(max_length=64)
    total_assets = models.CharField(max_length=64)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
