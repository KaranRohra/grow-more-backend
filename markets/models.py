from django.db import models


class Stock(models.Model):
    company_name = models.CharField(max_length=256)
    industry = models.CharField(max_length=256)
    nse_symbol = models.CharField(max_length=256, unique=True)
    bse_symbol = models.CharField(max_length=256, unique=True)
    yahoo_symbol = models.CharField(max_length=256, unique=True)
    isin_code = models.CharField(max_length=256, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.company_name}__{self.id}"


class Cashflow(models.Model):
    year = models.CharField(max_length=32)
    cash_from_operating_activity = models.CharField(max_length=128)
    cash_from_investing_activity = models.CharField(max_length=128)
    cash_from_financing_activity = models.CharField(max_length=128)
    net_cash_flow = models.CharField(max_length=128)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.stock.company_name}__{self.year}"


class ShareHoldingPattern(models.Model):
    quarter = models.CharField(max_length=32)
    promoter = models.CharField(max_length=3)
    fiis = models.CharField(max_length=3)
    diis = models.CharField(max_length=3)
    public = models.CharField(max_length=3)
    government = models.CharField(max_length=3)
    other = models.CharField(max_length=3)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.stock.company_name}__{self.quarter}"


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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.stock.company_name}__{self.quarter}"
