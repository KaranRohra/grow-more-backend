from rest_framework import serializers
from portfolio import models
from markets import serializers as market_serializer


class HoldingSerializer(serializers.ModelSerializer):
    stock = market_serializer.StockSerializer()

    class Meta:
        model = models.Holding
        fields = "__all__"

class OrderHistory(serializers.ModelSerializer):
    stock = market_serializer.StockSerializer()

    class Meta:
        model = models.Order
        fields = "__all__"