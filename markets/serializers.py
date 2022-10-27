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


class QuarterlyResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QuarterlyResult
        fields = "__all__"


class ProfitAndLossSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProfitAndLoss
        fields = "__all__"


class BalanceSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BalanceSheet
        fields = "__all__"
