from django.contrib import admin
from markets import models
# Register your models here.


@admin.register(models.ProfitAndLoss)
class ProfitAndLossAdmin(admin.ModelAdmin):
    list_display = ("id", "stock")
