from rest_framework import serializers
from markets import models


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Stock
        fields = "__all__"


class CashflowSerializer(serializers.ModelSerializer):
    stock = StockSerializer()
    class Meta:
        model = models.Cashflow
        fields = "__all__"


class ShareHoldingPatternSerializer(serializers.ModelSerializer):
    stock = StockSerializer()
    class Meta:
        model = models.ShareHoldingPattern
        fields = "__all__"


class QuarterlyResultSerializer(serializers.ModelSerializer):
    stock = StockSerializer()
    class Meta:
        model = models.QuarterlyResult


class ProfitAndLossSerializer(serializers.ModelSerializer):
    stock = StockSerializer()
    class Meta:
        model = models.ProfitAndLoss


class BalanceSheetSerializer(serializers.ModelSerializer):
    stock = StockSerializer()
    class Meta:
        model = models.BalanceSheet
        fields = "__all__"
