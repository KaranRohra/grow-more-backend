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
