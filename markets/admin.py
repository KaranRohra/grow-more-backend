from django.contrib import admin
from markets import models


@admin.register(models.QuarterlyResult)
class QuarterlyResultAdmin(admin.ModelAdmin):
    list_display = ("id", "stock", "quarter")