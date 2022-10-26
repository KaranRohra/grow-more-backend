from rest_framework import serializers
from markets import models


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Stock
        fields = "__all__"


class CashflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cashflow
        fields = "__all__"


class ShareHoldingPatternSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ShareHoldingPattern
        fields = "__all__"
