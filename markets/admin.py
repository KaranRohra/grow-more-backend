from django.contrib import admin
from markets import models


@admin.register(models.BalanceSheet)
class BalanceSheetAdmin(admin.ModelAdmin):
    list_display = ("id", "stock")
