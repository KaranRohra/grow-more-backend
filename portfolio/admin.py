from django.contrib import admin
from portfolio import models


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "order_type", "stock")


@admin.register(models.Holding)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ("user", "quantity", "stock", "price")
    