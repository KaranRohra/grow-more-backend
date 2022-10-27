from django.contrib import admin
from markets import models


@admin.register(models.Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("id", "company_name", "nse_symbol")


@admin.register(models.ShareHoldingPattern)
class ShareHoldingPatternAdmin(admin.ModelAdmin):
    list_display = ("id", "stock")


@admin.register(models.Cashflow)
class ShareHoldingPatternAdmin(admin.ModelAdmin):
    list_display = ("id", "stock")


@admin.register(models.QuarterlyResult)
class QuarterlyResultAdmin(admin.ModelAdmin):
    list_display = ("id", "stock", "quarter")


@admin.register(models.ProfitAndLoss)
class ProfitAndLossAdmin(admin.ModelAdmin):
    list_display = ("id", "stock")


@admin.register(models.BalanceSheet)
class BalanceSheetAdmin(admin.ModelAdmin):
    list_display = ("id", "stock")
