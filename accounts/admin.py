from django.contrib import admin
from accounts import models


@admin.register(models.Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("user", "balance")
